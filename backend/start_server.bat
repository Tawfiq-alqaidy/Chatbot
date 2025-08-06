@echo off
echo 🚀 Starting Ollama Chat Backend Server...
echo =====================================

REM Change to backend directory
cd /d "%~dp0"

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Check if packages are installed
echo 📦 Checking dependencies...
python -c "import fastapi, uvicorn, ollama; print('✅ All packages installed')" 2>nul
if errorlevel 1 (
    echo ⚠️  Installing missing packages...
    pip install fastapi uvicorn pydantic pydantic-settings ollama httpx python-multipart
)

REM Start the server
echo 🎯 Starting FastAPI server...
echo 📡 Server will be available at: http://localhost:8001
echo 📚 API docs available at: http://localhost:8001/docs
echo 🛑 Press Ctrl+C to stop the server
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
