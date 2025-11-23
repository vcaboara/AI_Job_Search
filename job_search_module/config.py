import os
from typing import Dict, Any

def load_config() -> Dict[str, Any]:
    """
    Loads configuration settings for the application.
    Currently checks for GEMINI_MODEL_NAME environment variable.
    """
    config = {
        "GEMINI_MODEL_NAME": os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash-preview-09-2025")
    }
    return config
