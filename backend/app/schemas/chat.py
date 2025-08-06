from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str
    model: Optional[str] = "mistral:latest"


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    response: str
    model: str
    timestamp: str


class HealthResponse(BaseModel):
    """Response model for health check endpoint"""
    status: str
    message: str
    ollama_status: str
