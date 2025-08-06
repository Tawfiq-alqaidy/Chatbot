"""
Quick check to see if Ollama is running and has the Mistral model
"""
import subprocess
import sys

def check_ollama():
    print("🔍 Checking Ollama status...")
    
    try:
        # Check if ollama command is available
        result = subprocess.run(['ollama', 'list'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Ollama is running!")
            
            # Check for mistral model
            if 'mistral' in result.stdout.lower():
                print("✅ Mistral model is available!")
                return True
            else:
                print("⚠️  Mistral model not found. Available models:")
                print(result.stdout)
                print("\n🔧 To install Mistral, run:")
                print("   ollama pull mistral:latest")
                return False
        else:
            print("❌ Ollama is not responding properly")
            print(f"Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Ollama command timed out")
        return False
    except FileNotFoundError:
        print("❌ Ollama is not installed or not in PATH")
        print("📥 Please install Ollama from: https://ollama.ai/")
        return False
    except Exception as e:
        print(f"❌ Error checking Ollama: {e}")
        return False

def test_ollama_connection():
    print("\n🧪 Testing Ollama API connection...")
    
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        
        if response.status_code == 200:
            print("✅ Ollama API is accessible!")
            models = response.json().get('models', [])
            print(f"📚 Found {len(models)} models")
            return True
        else:
            print(f"❌ Ollama API returned status {response.status_code}")
            return False
            
    except ImportError:
        print("⚠️  requests module not available, skipping API test")
        return True  # Don't fail if requests isn't installed
    except Exception as e:
        print(f"❌ Error connecting to Ollama API: {e}")
        return False

if __name__ == "__main__":
    print("🤖 Ollama Chat - Pre-flight Check")
    print("=" * 35)
    
    ollama_ok = check_ollama()
    api_ok = test_ollama_connection()
    
    print("\n" + "=" * 35)
    if ollama_ok and api_ok:
        print("🎉 All checks passed! Ready to start the chat server.")
        print("\n💡 Next steps:")
        print("   1. Run: start_server.bat")
        print("   2. Open frontend/index.html in your browser")
        print("   3. Start chatting!")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        
    print("\n🔧 If you need help:")
    print("   - Make sure Ollama is installed and running")
    print("   - Run 'ollama serve' if Ollama isn't running")
    print("   - Run 'ollama pull mistral:latest' to get the model")
