import ollama
import httpx
from typing import Dict, Any
from datetime import datetime
from app.core.config import settings


class OllamaService:
    """Service for interacting with Ollama LLM"""
    
    def __init__(self):
        self.client = ollama.Client(host=settings.ollama_host)
        self.default_model = settings.default_model
    
    async def generate_response(self, message: str, model: str = None) -> Dict[str, Any]:
        """
        Generate a response from Ollama LLM
        
        Args:
            message: User input message
            model: Model name to use (defaults to configured model)
            
        Returns:
            Dictionary containing response and metadata
        """
        if not model:
            model = self.default_model
            
        try:
            # Generate response using Ollama
            response = self.client.chat(
                model=model,
                messages=[
                    {
                        'role': 'user',
                        'content': message,
                    },
                ],
                stream=False
            )
            
            return {
                "response": response['message']['content'],
                "model": model,
                "timestamp": datetime.now().isoformat(),
                "success": True
            }
            
        except Exception as e:
            return {
                "response": f"Error generating response: {str(e)}",
                "model": model,
                "timestamp": datetime.now().isoformat(),
                "success": False,
                "error": str(e)
            }
    
    async def stream_response(self, message: str, model: str = None):
        """
        Generate a streaming response from Ollama LLM
        
        Args:
            message: User input message
            model: Model name to use (defaults to configured model)
            
        Yields:
            Dictionary containing response chunks and metadata
        """
        if not model:
            model = self.default_model
            
        try:
            # Generate streaming response using Ollama
            stream = self.client.chat(
                model=model,
                messages=[
                    {
                        'role': 'user',
                        'content': message,
                    },
                ],
                stream=True
            )
            
            full_response = ""
            for chunk in stream:
                if 'message' in chunk and 'content' in chunk['message']:
                    content = chunk['message']['content']
                    full_response += content
                    
                    yield {
                        "chunk": content,
                        "full_response": full_response,
                        "model": model,
                        "timestamp": datetime.now().isoformat(),
                        "success": True,
                        "done": chunk.get('done', False)
                    }
                    
        except Exception as e:
            yield {
                "chunk": "",
                "full_response": f"Error generating response: {str(e)}",
                "model": model,
                "timestamp": datetime.now().isoformat(),
                "success": False,
                "error": str(e),
                "done": True
            }
    
    async def check_ollama_status(self) -> Dict[str, Any]:
        """
        Check if Ollama is running and accessible
        
        Returns:
            Dictionary containing status information
        """
        try:
            # Try to connect to Ollama
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{settings.ollama_host}/api/tags")
                
            if response.status_code == 200:
                models = response.json().get("models", [])
                return {
                    "status": "healthy",
                    "models_available": len(models),
                    "models": [model["name"] for model in models]
                }
            else:
                return {
                    "status": "unhealthy",
                    "error": f"HTTP {response.status_code}"
                }
                
        except Exception as e:
            return {
                "status": "unreachable",
                "error": str(e)
            }
    
    def list_models(self) -> Dict[str, Any]:
        """
        List available models in Ollama
        
        Returns:
            Dictionary containing available models
        """
        try:
            models = self.client.list()
            return {
                "success": True,
                "models": [model["name"] for model in models["models"]]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "models": []
            }


# Global service instance
ollama_service = OllamaService()
