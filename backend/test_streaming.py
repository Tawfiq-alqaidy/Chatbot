import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Test the new streaming functionality
import asyncio
from app.services.ollama_service import ollama_service

async def test_streaming():
    print("Testing streaming functionality...")
    
    test_message = "Hello, how are you?"
    
    async for chunk in ollama_service.stream_response(test_message):
        if chunk.get('success'):
            print(f"Chunk: '{chunk.get('chunk', '')}'")
            if chunk.get('done'):
                print("Streaming complete!")
                break
        else:
            print(f"Error: {chunk.get('error')}")
            break

if __name__ == "__main__":
    asyncio.run(test_streaming())
