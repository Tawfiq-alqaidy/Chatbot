#!/bin/bash

# Ollama Chat Setup Script
# This script helps you set up the Ollama Chat project quickly

echo "🤖 Welcome to Ollama Chat Setup!"
echo "================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10+ first."
    exit 1
fi

echo "✅ Python 3 found"

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is not installed."
    echo "📥 Please install Ollama first: https://ollama.ai/"
    echo "   Then run: ollama pull mistral:latest"
    exit 1
fi

echo "✅ Ollama found"

# Check if mistral:latest model is available
if ! ollama list | grep -q "mistral:latest"; then
    echo "⚠️  Mistral model not found. Downloading..."
    ollama pull mistral:latest
    if [ $? -ne 0 ]; then
        echo "❌ Failed to download mistral model"
        exit 1
    fi
fi

echo "✅ Mistral model available"

# Setup backend
echo ""
echo "📦 Setting up backend..."
cd backend

# Create virtual environment
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

echo "✅ Backend setup complete"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
fi

cd ..

echo ""
echo "🎉 Setup complete!"
echo ""
echo "🚀 To start the application:"
echo ""
echo "1. Start the backend server:"
echo "   cd backend"
echo "   source .venv/bin/activate"
echo "   uvicorn app.main:app --reload"
echo ""
echo "2. Open the frontend:"
echo "   cd frontend"
echo "   python3 -m http.server 3000"
echo "   # Then open http://localhost:3000"
echo ""
echo "📚 For more information, see README.md"
echo ""
echo "Happy chatting! 🤖💬"
