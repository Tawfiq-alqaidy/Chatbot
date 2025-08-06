from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.schemas import ChatRequest, ChatResponse, HealthResponse
from app.services import ollama_service
import json

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint - send a message to Ollama LLM and get a response
    """
    try:
        result = await ollama_service.generate_response(
            message=request.message,
            model=request.model
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate response: {result.get('error', 'Unknown error')}"
            )
        
        return ChatResponse(
            response=result["response"],
            model=result["model"],
            timestamp=result["timestamp"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Streaming chat endpoint - stream response chunks as they're generated
    """
    try:
        async def generate():
            async for chunk in ollama_service.stream_response(
                message=request.message,
                model=request.model
            ):
                if chunk.get("success", False):
                    yield f"data: {json.dumps(chunk)}\n\n"
                else:
                    yield f"data: {json.dumps({'error': chunk.get('error', 'Unknown error')})}\n\n"
                    break
            
            # Send end signal
            yield f"data: {json.dumps({'done': True})}\n\n"
        
        return StreamingResponse(
            generate(),
            media_type="text/plain",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "text/plain; charset=utf-8"
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint - verify API and Ollama status
    """
    try:
        ollama_status_result = await ollama_service.check_ollama_status()
        ollama_status = ollama_status_result["status"]
        
        return HealthResponse(
            status="healthy" if ollama_status == "healthy" else "degraded",
            message="API is running",
            ollama_status=ollama_status
        )
        
    except Exception as e:
        return HealthResponse(
            status="unhealthy",
            message=f"Health check failed: {str(e)}",
            ollama_status="unknown"
        )


@router.get("/models")
async def list_models():
    """
    List available Ollama models
    """
    try:
        result = ollama_service.list_models()
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list models: {str(e)}"
        )
