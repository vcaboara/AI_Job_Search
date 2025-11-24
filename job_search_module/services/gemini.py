import os
from typing import List, Optional

from google import genai
from google.genai import types

from job_search_module.services.base import AbstractAIService

class GeminiService(AbstractAIService):
    """Concrete implementation of AbstractAIService for the Gemini API."""

    def __init__(
        self,
        model_name: str = "gemini-2.5-flash-preview-09-2025",
        client: Optional[genai.Client] = None
    ):
        self.model_name = model_name
        self.client = client if client else genai.Client()

    def generate_content(
        self,
        contents: List[types.Part],
        response_schema: types.Schema,
        temperature: float = 0.2,
        system_instruction: Optional[str] = None # Added for compatibility with core.py
    ) -> str:
        """
        Generates content using the Gemini API.

        Args:
            contents: A list of content parts to send to the model.
            response_schema: The schema for the expected JSON response.
            temperature: Controls the randomness of the output.
            system_instruction: Optional system instruction for the model.

        Returns:
            A JSON string conforming to the response_schema.
        """
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    response_schema=response_schema,
                    temperature=temperature
                )
            )
            return response.text
        except Exception as e:
            # In a real application, you might want more sophisticated error handling
            print(f"An error occurred during Gemini API call: {e}")
            return "[]" # Return an empty JSON array on error to conform to expected output type
