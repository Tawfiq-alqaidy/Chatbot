@echo off
REM Ollama Chat Setup Script for Windows
REM This script helps you set up the Ollama Chat project quickly

echo 🤖 Welcome to Ollama Chat Setup!
echo =================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.10+ first.
    pause
    exit /b 1
)

echo ✅ Python found

REM Check if Ollama is installed
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Ollama is not installed.
    echo 📥 Please install Ollama first: https://ollama.ai/
    echo    Then run: ollama pull mistral:latest
    pause
    exit /b 1
)

echo ✅ Ollama found

REM Check if mistral:latest model is available
ollama list | findstr "mistral:latest" >nul
if %errorlevel% neq 0 (
    echo ⚠️  Mistral model not found. Downloading...
    ollama pull mistral:latest
    if %errorlevel% neq 0 (
        echo ❌ Failed to download mistral model
        pause
        exit /b 1
    )
)

echo ✅ Mistral model available

REM Setup backend
echo.
echo 📦 Setting up backend...
cd backend

REM Create virtual environment
if not exist ".venv" (
    echo Creating Python virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ Failed to install Python dependencies
    pause
    exit /b 1
)

echo ✅ Backend setup complete

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo 📝 Creating .env file...
    copy .env.example .env
)

cd ..

echo.
echo 🎉 Setup complete!
echo.
echo 🚀 To start the application:
echo.
echo 1. Start the backend server:
echo    cd backend
echo    .venv\Scripts\activate
echo    uvicorn app.main:app --reload
echo.
echo 2. Open the frontend:
echo    cd frontend
echo    python -m http.server 3000
echo    # Then open http://localhost:3000
echo.
echo 📚 For more information, see README.md
echo.
echo Happy chatting! 🤖💬
pause
