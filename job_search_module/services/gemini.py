import os
from typing import List, Optional

import google.generativeai as generativeai_sdk # Changed import
from google.genai import types # Still needed for types.Part and types.Schema

from job_search_module.services.base import AbstractAIService

class GeminiService(AbstractAIService):
    """Concrete implementation of AbstractAIService for the Gemini API."""

    def __init__(
        self,
        model_name: str = "gemini-2.5-flash-preview-09-2025",
        api_key: Optional[str] = None # Changed to accept API key directly
    ):
        self.model_name = model_name
        if api_key:
            generativeai_sdk.configure(api_key=api_key) # Configure the SDK
        self.model = generativeai_sdk.GenerativeModel(self.model_name) # Initialize GenerativeModel

    def generate_content(
        self,
        contents: List[types.Part],
        response_schema: types.Schema,
        temperature: float = 0.2,
        system_instruction: Optional[str] = None
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
            response = self.model.generate_content( # Call generate_content on the model
                contents=contents,
                generation_config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    response_schema=response_schema,
                    temperature=temperature
                )
            )
            return response.text
        except Exception as e:
            print(f"An error occurred during Gemini API call: {e}")
            return "[]"
