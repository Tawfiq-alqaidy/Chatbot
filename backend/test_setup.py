"""
Quick test script to verify the Ollama Chat setup
Run this after setting up the project to ensure everything works
"""

import asyncio
import httpx
import sys
import time
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent / "app"))

try:
    from app.services.ollama_service import ollama_service
    from app.core.config import settings
except ImportError as e:
    print(f"❌ Failed to import app modules: {e}")
    print("Make sure you're running this from the backend directory")
    sys.exit(1)


async def test_ollama_connection():
    """Test connection to Ollama"""
    print("🔍 Testing Ollama connection...")
    
    try:
        status = await ollama_service.check_ollama_status()
        if status["status"] == "healthy":
            print(f"✅ Ollama is running and healthy")
            if "models" in status:
                print(f"📚 Available models: {', '.join(status['models'])}")
        else:
            print(f"⚠️  Ollama status: {status['status']}")
            if "error" in status:
                print(f"   Error: {status['error']}")
    except Exception as e:
        print(f"❌ Failed to connect to Ollama: {e}")
        return False
    
    return True


async def test_chat_functionality():
    """Test basic chat functionality"""
    print("\n💬 Testing chat functionality...")
    
    try:
        test_message = "Hello! Please respond with just 'Test successful' and nothing else."
        
        print(f"   Sending: {test_message}")
        result = await ollama_service.generate_response(test_message)
        
        if result["success"]:
            print(f"✅ Chat test successful!")
            print(f"   Model: {result['model']}")
            print(f"   Response: {result['response'][:100]}...")
        else:
            print(f"❌ Chat test failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Chat test failed with exception: {e}")
        return False
    
    return True


def test_frontend_files():
    """Check if frontend files exist"""
    print("\n📁 Checking frontend files...")
    
    frontend_dir = Path(__file__).parent.parent / "frontend"
    required_files = ["index.html", "style.css", "script.js"]
    
    all_exist = True
    for file_name in required_files:
        file_path = frontend_dir / file_name
        if file_path.exists():
            print(f"✅ {file_name} exists")
        else:
            print(f"❌ {file_name} missing")
            all_exist = False
    
    return all_exist


async def main():
    """Run all tests"""
    print("🧪 Ollama Chat Setup Test")
    print("=" * 30)
    
    # Test configuration
    print(f"📋 Configuration:")
    print(f"   Ollama Host: {settings.ollama_host}")
    print(f"   Default Model: {settings.default_model}")
    print(f"   API Prefix: {settings.api_prefix}")
    
    # Run tests
    tests = [
        ("Ollama Connection", test_ollama_connection()),
        ("Chat Functionality", test_chat_functionality()),
        ("Frontend Files", test_frontend_files())
    ]
    
    results = []
    for test_name, test_coro in tests:
        if asyncio.iscoroutine(test_coro):
            result = await test_coro
        else:
            result = test_coro
        results.append((test_name, result))
    
    # Summary
    print("\n📊 Test Summary:")
    print("=" * 20)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 30)
    if all_passed:
        print("🎉 All tests passed! Your Ollama Chat setup is ready!")
        print("\n🚀 Next steps:")
        print("   1. Start the backend: uvicorn app.main:app --reload")
        print("   2. Open frontend/index.html in your browser")
        print("   3. Start chatting!")
    else:
        print("❌ Some tests failed. Please check the setup:")
        print("   - Ensure Ollama is running: ollama serve")
        print("   - Ensure llama3 is installed: ollama pull llama3")
        print("   - Check all files are in place")
    
    return all_passed


if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)
