"""
Simple verification script for Mistral configuration
"""

import os
from pathlib import Path

print("🔍 Checking Mistral Configuration...")
print("=" * 40)

# Check backend config file
backend_config = Path(__file__).parent / "app" / "core" / "config.py"
if backend_config.exists():
    try:
        content = backend_config.read_text(encoding='utf-8')
        if 'default_model: str = "mistral:latest"' in content:
            print("✅ Backend config: mistral:latest")
        else:
            print("❌ Backend config: NOT set to mistral:latest")
    except Exception as e:
        print(f"⚠️  Could not read backend config: {e}")
else:
    print("❌ Backend config file not found")

# Check .env.example
env_example = Path(__file__).parent / ".env.example"
if env_example.exists():
    try:
        content = env_example.read_text(encoding='utf-8')
        if 'DEFAULT_MODEL=mistral:latest' in content:
            print("✅ Environment example: mistral:latest")
        else:
            print("❌ Environment example: NOT set to mistral:latest")
    except Exception as e:
        print(f"⚠️  Could not read .env.example: {e}")
else:
    print("❌ .env.example file not found")

# Check frontend script
frontend_script = Path(__file__).parent.parent / "frontend" / "script.js"
if frontend_script.exists():
    try:
        content = frontend_script.read_text(encoding='utf-8')
        if 'this.currentModel = "mistral:latest"' in content:
            print("✅ Frontend script: mistral:latest")
        else:
            print("❌ Frontend script: NOT set to mistral:latest")
    except Exception as e:
        print(f"⚠️  Could not read frontend script: {e}")
else:
    print("❌ Frontend script file not found")

# Check frontend HTML
frontend_html = Path(__file__).parent.parent / "frontend" / "index.html"
if frontend_html.exists():
    try:
        content = frontend_html.read_text(encoding='utf-8')
        if 'id="current-model">mistral:latest' in content:
            print("✅ Frontend HTML: mistral:latest")
        else:
            print("❌ Frontend HTML: NOT set to mistral:latest")
    except Exception as e:
        print(f"⚠️  Could not read frontend HTML: {e}")
else:
    print("❌ Frontend HTML file not found")

print("\n" + "=" * 40)
print("🎯 Configuration Summary:")
print("   All files should show mistral:latest as the default model")
print("\n💡 Next steps:")
print("   1. Make sure Ollama is running: ollama serve")
print("   2. Pull the Mistral model: ollama pull mistral:latest")
print("   3. Start the backend: uvicorn app.main:app --reload")
print("   4. Open the frontend in your browser")
print("\n🚀 Ready to chat with Mistral!")
