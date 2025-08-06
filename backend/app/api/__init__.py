from fastapi import APIRouter
from .chat import router as chat_router

# Main API router
api_router = APIRouter()

# Include sub-routers
api_router.include_router(chat_router, tags=["chat"])

__all__ = ["api_router"]
