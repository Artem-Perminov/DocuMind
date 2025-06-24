"""
Configuration management for the AI Agent.
"""

import os
from typing import Optional
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings(BaseModel):
    """Application settings."""

    # API Configuration
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    site_url: str = os.getenv("SITE_URL", "http://localhost:3000")
    site_name: str = os.getenv("SITE_NAME", "AI Agent Template")

    # Model Configuration
    model_name: str = os.getenv("MODEL_NAME", "deepseek/deepseek-r1-0528:free")
    max_tokens: int = int(os.getenv("MAX_TOKENS", "1000"))
    temperature: float = float(os.getenv("TEMPERATURE", "0.7"))

    # Agent Configuration
    max_iterations: int = int(os.getenv("MAX_ITERATIONS", "10"))
    timeout_seconds: int = int(os.getenv("TIMEOUT_SECONDS", "30"))

    # Development
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    def validate_api_key(self) -> bool:
        """Validate that API key is set."""
        return bool(
            self.openrouter_api_key
            and self.openrouter_api_key != "your_openrouter_api_key_here"
        )


# Global settings instance
settings = Settings()
