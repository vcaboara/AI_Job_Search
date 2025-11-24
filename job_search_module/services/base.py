from abc import ABC, abstractmethod
from typing import List

from google.genai import types

class AbstractAIService(ABC):
    """Abstract Base Class for AI services."""

    @abstractmethod
    def generate_content(self,
        contents: List[types.Part],
        response_schema: types.Schema,
        temperature: float = 0.2
    ) -> str:
        """
        Abstract method to generate content using an AI model.

        Args:
            contents: A list of content parts to send to the model.
            response_schema: The schema for the expected JSON response.
            temperature: Controls the randomness of the output.

        Returns:
            A JSON string conforming to the response_schema.
        """
        pass
