from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import api_router
from app.core.config import settings

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    debug=settings.debug,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.api_prefix)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Ollama Chat API",
        "version": settings.version,
        "docs": "/docs"
    }


@app.get("/ping")
async def ping():
    """Simple ping endpoint"""
    return {"message": "pong"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
