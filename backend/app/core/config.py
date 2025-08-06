from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""
    
    # App config
    app_name: str = "Ollama Chat API"
    version: str = "1.0.0"
    debug: bool = False
    
    # CORS settings
    allowed_origins: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "*"  # Allow all origins for development
    ]
    
    # Ollama settings
    ollama_host: str = "http://localhost:11434"
    default_model: str = "mistral:latest"
    
    # API settings
    api_prefix: str = "/api/v1"
    
    class Config:
        env_file = ".env"


# Global settings instance
settings = Settings()
