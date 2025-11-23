import os
import json
from typing import List, Dict, Any, Optional

from google import genai
from google.genai import types
from pydantic import BaseModel, Field

from job_search_module.config import load_config

# Load configuration
app_config = load_config()

# --- Pydantic Models for Data Validation ---

class JobLead(BaseModel):
    """Defines the structure for a single job lead."""
    title: str = Field(description="The exact job title.")
    company: str = Field(description="The name of the hiring company.")
    description: str = Field(description="A concise, 1-2 sentence summary of the primary responsibilities and how they align with the user's context/query.")
    link: str = Field(description="The direct URL to the job posting.")

# --- Core Functionality ---

def find_job_leads(
    user_query: str,
    context_filepath: Optional[str] = None,
    client: Optional[genai.Client] = None
) -> List[JobLead]:
    """
    Finds job leads using the Gemini API, incorporating context and structured output.

    Args:
        user_query: The main query (e.g., "DevOps Engineer for climate impact").
        context_filepath: Optional path to a file (e.g., resume image) for context.
        client: Optional initialized genai.Client instance.

    Returns:
        A list of JobLead objects.
    """
    if client is None:
        # Client automatically uses the GEMINI_API_KEY environment variable
        client = genai.Client()

    # 1. System Instruction (Persona & Rules)
    system_instruction_parts = [
        "You are an expert strategic career researcher and job lead analyst. Your goal is to find highly relevant, open job postings.",
        "Critically, you MUST use the provided context to filter and prioritize the job search results.",
        "Prioritize jobs related to DevOps, CI/CD, and Python, especially within the Climate/Sustainability sector or roles that align with the AIF Mandates (supporting Native Americans, immigrants, veterans, and orphans/ages).",
        "Your final output MUST strictly follow the provided JSON schema."
    ]
    system_prompt = "\n".join(system_instruction_parts)

    # 2. Build Content Parts
    content_parts = []

    if context_filepath:
        print(f"Loading context file: {context_filepath}")
        mime_type = "application/octet-stream"

        # Simple file reading and mime type inference (basic handling)
        try:
            with open(context_filepath, "rb") as f:
                file_bytes = f.read()
        except FileNotFoundError:
            print(f"Error: Context file not found at {context_filepath}. Skipping file context.")
            file_bytes = None

        if file_bytes:
            # Basic MIME type detection based on extension
            if context_filepath.lower().endswith(('.png', '.jpg', '.jpeg')):
                mime_type = "image/jpeg" # Using jpeg as a common fallback
                print(f"Inferred MIME type: {mime_type}")
                content_parts.append(types.Part.from_bytes(data=file_bytes, mime_type=mime_type))
                content_parts.append(types.Part(text="Use the uploaded file as a resume or context document to refine and prioritize your job search results."))
            elif context_filepath.lower().endswith(('.txt', '.md', '.docx')):
                # For text-based files, append the content as text
                try:
                    text_content = file_bytes.decode('utf-8')
                    system_prompt += f"\n\n--- TEXT CONTEXT FOR PRIORITIZATION ---\nCore Resume/Skills Profile:\n\n{text_content}\n---------------------------------------"
                    print("Text content integrated into system prompt.")
                except UnicodeDecodeError:
                    print("Warning: Could not decode file as UTF-8 text. Skipping content integration.")

    # Add the main user query
    content_parts.append(types.Part(text=user_query))

    # 3. Define the Structured Response
    single_job_lead_schema = types.Schema(
        type="object",
        properties={
            "title": types.Schema(type="string", description="The exact job title."),
            "company": types.Schema(type="string", description="The name of the hiring company."),
            "description": types.Schema(type="string", description="A concise, 1-2 sentence summary of the primary responsibilities and how they align with the user's context/query."),
            "link": types.Schema(type="string", description="The direct URL to the job posting."),
        },
        required=["title", "company", "description", "link"]
    )

    response_schema = types.Schema(
        type="array",
        items=single_job_lead_schema
    )

    # 4. API Call
    try:
        response = client.models.generate_content(
            model=app_config["GEMINI_MODEL_NAME"],
            contents=content_parts,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                response_schema=response_schema,
                temperature=0.2
            )
        )

        json_output = response.text
        parsed_leads = [JobLead.model_validate(item) for item in json.loads(json_output)]

        return parsed_leads

    except Exception as e:
        print(f"An error occurred during the Gemini API call: {e}")
        return []
