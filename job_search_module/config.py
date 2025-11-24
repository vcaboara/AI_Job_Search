import os
from typing import Dict, Any

def load_config() -> Dict[str, Any]:
    """
    Loads configuration settings for the application.
    Includes AI service type and specific model names.
    """
    config = {
        "AI_SERVICE_TYPE": os.getenv("AI_SERVICE_TYPE", "gemini"),
        "GEMINI_MODEL_NAME": os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash-preview-09-2025"),
        "OPENAI_MODEL_NAME": os.getenv("OPENAI_MODEL_NAME", "gpt-4o") # Placeholder for future OpenAI integration
    }
    return config
