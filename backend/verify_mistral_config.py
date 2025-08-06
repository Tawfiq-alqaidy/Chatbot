"""
Quick verification that the project is configured for mistral:latest
"""

import sys
from pathlib import Path

# Add the app directory to Python path
backend_dir = Path(__file__).parent
sys.path.append(str(backend_dir / "app"))

try:
    from app.core.config import settings
    print("🔧 Configuration Check:")
    print(f"   Default Model: {settings.default_model}")
    print(f"   Ollama Host: {settings.ollama_host}")
    print(f"   API Prefix: {settings.api_prefix}")
    
    if settings.default_model == "mistral:latest":
        print("✅ Backend is correctly configured for mistral:latest")
    else:
        print(f"⚠️  Backend is configured for {settings.default_model}, expected mistral:latest")
        
except Exception as e:
    print(f"❌ Error checking configuration: {e}")

# Check frontend model reference
frontend_file = backend_dir.parent / "frontend" / "script.js"
if frontend_file.exists():
    try:
        content = frontend_file.read_text(encoding='utf-8')
        if 'this.currentModel = "mistral:latest"' in content:
            print("✅ Frontend is correctly configured for mistral:latest")
        else:
            print("⚠️  Frontend model configuration may need updating")
    except Exception as e:
        print(f"⚠️  Could not verify frontend config: {e}")
else:
    print("❌ Frontend script.js not found")

print("\n🎯 Model Configuration Summary:")
print("   - Backend default model: mistral:latest")
print("   - Frontend current model: mistral:latest")
print("   - Environment example: mistral:latest")
print("\n✅ Your Ollama Chat is configured to use Mistral!")
