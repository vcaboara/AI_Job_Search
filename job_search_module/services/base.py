from abc import ABC, abstractmethod
from typing import List, Optional

from google.generativeai.types import Part, Schema # Explicitly import Part and Schema

class AbstractAIService(ABC):
    """Abstract Base Class for AI services."""

    @abstractmethod
    def generate_content(
        self,
        contents: List[Part],
        response_schema: Schema,
        temperature: float = 0.2,
        system_instruction: Optional[str] = None
    ) -> str:
        """
        Abstract method to generate content using an AI model.

        Args:
            contents: A list of content parts to send to the model.
            response_schema: The schema for the expected JSON response.
            temperature: Controls the randomness of the output.
            system_instruction: Optional system instruction for the model.

        Returns:
            A JSON string conforming to the response_schema.
        """
        pass
