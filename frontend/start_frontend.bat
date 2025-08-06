@echo off
echo 🌐 Starting Ollama Chat Frontend...
echo ==================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not available. Please install Python first.
    pause
    exit /b 1
)

echo 📁 Current directory: frontend
echo 🚀 Starting HTTP server on http://localhost:3000
echo 🌍 Frontend will be available at: http://localhost:3000
echo 🛑 Press Ctrl+C to stop the server
echo.
echo 💡 After the server starts:
echo    1. Open your browser
echo    2. Go to http://localhost:3000
echo    3. Start chatting with Mistral!
echo.

python -m http.server 3000
