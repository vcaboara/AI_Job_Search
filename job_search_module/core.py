import os
import json
from typing import List, Dict, Any, Optional

from pydantic import BaseModel, Field
from google.genai import types # FIXED: Changed from google.generativeai back to google.genai for local compatibility

from job_search_module.config import load_config
from job_search_module.services.base import AbstractAIService

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
    ai_service: AbstractAIService,
    context_text: Optional[str] = None,
    context_image_filepath: Optional[str] = None
) -> List[JobLead]:
    """
    Finds job leads using an AI service, incorporating context and structured output.

    Args:
        user_query: The main query (e.g., "DevOps Engineer for climate impact").
        ai_service: An instance of a class implementing AbstractAIService.
        context_text: Optional text content (e.g., extracted from resume) for context.
        context_image_filepath: Optional path to an image file (e.g., resume image) for context.

    Returns:
        A list of JobLead objects.
    """

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

    if context_text:
        system_prompt += f"\n\n--- TEXT CONTEXT FOR PRIORITIZATION ---\nCore Resume/Skills Profile:\n\n{context_text}\n---------------------------------------"
        print("Text content integrated into system prompt.")

    if context_image_filepath:
        print(f"Loading image context file: {context_image_filepath}")
        try:
            with open(context_image_filepath, "rb") as f:
                file_bytes = f.read()
            mime_type = "image/jpeg" # Assuming only jpeg/png for simplicity with multi-modal AI
            if context_image_filepath.lower().endswith(('.png')):
                mime_type = "image/png"

            content_parts.append(types.Part.from_bytes(data=file_bytes, mime_type=mime_type))
            content_parts.append(types.Part(text="Use the uploaded image as a resume or context document to refine and prioritize your job search results."))
        except FileNotFoundError:
            print(f"Error: Image context file not found at {context_image_filepath}. Skipping image context.")
        except Exception as e:
            print(f"Error loading image file {context_image_filepath}: {e}. Skipping image context.")

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

    # 4. API Call using the provided AI service
    try:
        # Call generate_content on the ai_service instance
        json_output = ai_service.generate_content(
            contents=content_parts,
            response_schema=response_schema,
            temperature=0.2,
            system_instruction=system_prompt # Pass system_instruction to the service
        )

        # Parse the JSON string into the desired Python list of Pydantic models
        parsed_leads = [JobLead.model_validate(item) for item in json.loads(json_output)]

        return parsed_leads

    except Exception as e:
        print(f"An error occurred during the AI service call: {e}")
        return []
