# 🧠 Ollama Chat - Fullstack LLM Copilot Template

<div align="center">

![Ollama Chat](https://img.shields.io/badge/Ollama-Chat-brightgreen?style=for-the-badge&logo=robot)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

_A production-ready fullstack chatbot template for running LLMs locally with Ollama_

[Features](#-features) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [API](#-api-reference) • [Development](#-development)

</div>

## 📌 Overview

Ollama Chat is a production-ready fullstack chatbot agent template designed to run Large Language Models (LLMs) locally via Ollama. It provides a clean architecture with modular design and clear frontend/backend separation, serving as a strong foundation for building your own private ChatGPT-like agent.

Perfect for:

- 🏠 **Local AI copilots** - Complete privacy, no data leaves your machine
- 🏢 **Internal company assistants** - Secure, self-hosted AI tools
- 🔬 **LLM experimentation** - Easy model switching and testing
- 🎓 **Learning AI development** - Clean codebase for education

## 🚀 Features

- 🧠 **Local LLM Integration** - Run any Ollama model (Llama3, Mistral, CodeLlama, etc.)
- ⚡ **FastAPI Backend** - Modern, fast, and type-safe API with automatic documentation
- 🎨 **ChatGPT-like UI** - Responsive, dark/light theme, and mobile-friendly interface
- 🔌 **REST API Communication** - Clean separation between frontend and backend
- 🏗️ **Modular Architecture** - Maintainable, extendable, production-ready code
- 🔒 **100% Private** - All processing happens locally, zero external dependencies
- 🌙 **Dark Mode Support** - Built-in theme switching with persistence
- 📱 **Responsive Design** - Works seamlessly on desktop and mobile devices
- 🔄 **Real-time Status** - Connection monitoring and health checks
- ⚙️ **Model Switching** - Easy configuration for different LLM models
- ⚡ **Streaming Responses** - Real-time word-by-word response streaming
- 📜 **Smooth Scrolling** - Optimized chat interface with proper scroll handling

## 🧭 Project Structure

```
ollama-chat/
├── backend/                    # FastAPI backend service
│   ├── app/
│   │   ├── api/               # API routes and endpoints
│   │   │   ├── __init__.py
│   │   │   └── chat.py        # Chat and health endpoints
│   │   ├── services/          # Business logic layer
│   │   │   ├── __init__.py
│   │   │   └── ollama_service.py  # Ollama client integration
│   │   ├── schemas/           # Pydantic models
│   │   │   ├── __init__.py
│   │   │   └── chat.py        # Request/response models
│   │   ├── core/              # Configuration and settings
│   │   │   ├── __init__.py
│   │   │   └── config.py      # App configuration
│   │   ├── __init__.py
│   │   └── main.py            # FastAPI application entrypoint
│   └── requirements.txt       # Python dependencies
│
├── frontend/                   # Static web interface
│   ├── assets/                # Static assets (images, icons)
│   ├── index.html             # Main HTML structure
│   ├── style.css              # Styling and themes
│   └── script.js              # Frontend logic and API calls
│
└── README.md                  # Project documentation
```

## 🛠️ Tech Stack

| Layer             | Technology            | Purpose                                  |
| ----------------- | --------------------- | ---------------------------------------- |
| **Backend**       | FastAPI               | REST API server with automatic docs      |
|                   | Ollama Python Client  | LLM integration and model management     |
|                   | Pydantic              | Data validation and serialization        |
|                   | Uvicorn               | ASGI server for production deployment    |
| **Frontend**      | HTML5 + CSS3          | Modern, semantic markup and styling      |
|                   | Vanilla JavaScript    | Lightweight, no-framework frontend logic |
|                   | CSS Custom Properties | Theme system and responsive design       |
| **Communication** | REST/JSON             | Standard HTTP API communication          |
| **Runtime**       | Ollama                | Local LLM inference engine               |

## ⚡ Quick Start

### Prerequisites

- **Python 3.10+** installed
- **Ollama** installed and running ([Install Ollama](https://ollama.ai/))
- A compatible LLM model downloaded (e.g., `mistral:latest`)

### 1. Clone and Setup Backend

```bash
# Clone the repository
git clone https://github.com/Tawfiq-alqaidy/Chatbot.git
cd Chatbot

# Setup Python virtual environment
cd backend
python -m venv .venv

# Activate virtual environment
# Windows:
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Download and Start Ollama Model

```bash
# Download Mistral model (this may take a while)
ollama pull mistral:latest

# Verify Ollama is running
ollama list
```

### 3. Start the Backend Server

```bash
# From the backend directory
# Option 1: Using the custom runner (recommended)
python run_server.py

# Option 2: Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

# Option 3: Using the batch file (Windows)
start_server.bat
```

The API will be available at:

- **API Endpoint**: http://localhost:8001
- **Interactive Docs**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

### 4. Start the Frontend

```bash
# From the project root, open a new terminal
cd frontend

# Start the frontend server
python -m http.server 8080
```

The frontend will be available at: **http://localhost:8080**

### 5. Start Chatting! 🎉

1. Open your browser to http://localhost:8080
2. Wait for the "Connected" status indicator to turn green
3. Type your first message and press Enter
4. Enjoy real-time streaming responses from Mistral!

## 🔧 Configuration

### Backend Configuration

Edit `backend/app/core/config.py` to customize:

```python
class Settings(BaseSettings):
    # Ollama settings
    ollama_host: str = "http://localhost:11434"  # Ollama server URL
    default_model: str = "mistral:latest"         # Default model name

    # CORS settings
    allowed_origins: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"  # Allow all origins (development only!)
    ]

    # API settings
    api_prefix: str = "/api/v1"
```

### Frontend Configuration

Edit `frontend/script.js` to customize:

```javascript
const CONFIG = {
  API_BASE_URL: "http://localhost:8001/api/v1", // Backend API URL
  MAX_RETRIES: 3, // Request retry count
  RETRY_DELAY: 1000, // Delay between retries (ms)
  AUTO_SCROLL_DELAY: 100, // Auto-scroll delay (ms)
  TYPING_SPEED: 20, // Typing animation speed (ms)
};
```

### Environment Variables

Create a `.env` file in the backend directory:

```env
# App settings
DEBUG=True
APP_NAME="Ollama Chat API"

# Ollama settings
OLLAMA_HOST=http://localhost:11434
DEFAULT_MODEL=mistral:latest

# CORS settings (comma-separated)
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

## 📡 API Reference

### Chat Endpoint

**POST** `/api/v1/chat`

Send a message to the LLM and receive a complete response.

```json
// Request
{
  "message": "Hello, how are you?",
  "model": "mistral:latest"  // optional
}

// Response
{
  "response": "Hello! I'm doing well, thank you for asking. How can I help you today?",
  "model": "mistral:latest",
  "timestamp": "2024-01-20T10:30:00"
}
```

### Streaming Chat Endpoint

**POST** `/api/v1/chat/stream`

Send a message and receive a real-time streaming response.

```json
// Request
{
  "message": "Tell me a joke",
  "model": "mistral:latest"  // optional
}

// Response (Server-Sent Events)
data: {"chunk": "Why", "full_response": "Why", "model": "mistral:latest", "timestamp": "2024-01-20T10:30:00", "success": true, "done": false}
data: {"chunk": " did", "full_response": "Why did", "model": "mistral:latest", "timestamp": "2024-01-20T10:30:01", "success": true, "done": false}
...
data: {"done": true}
```

### Health Check

**GET** `/api/v1/health`

Check the status of the API and Ollama connection.

```json
// Response
{
  "status": "healthy",
  "message": "API is running",
  "ollama_status": "healthy"
}
```

### List Models

**GET** `/api/v1/models`

Get a list of available Ollama models.

```json
// Response
{
  "success": true,
  "models": ["mistral:latest", "llama3", "codellama"]
}
```

## 🔄 How It Works

1. **User Input**: User types a message in the frontend interface
2. **API Request**: JavaScript sends POST request to `/api/v1/chat`
3. **LLM Processing**: FastAPI backend forwards message to Ollama
4. **Model Response**: Ollama processes the message and returns response
5. **UI Update**: Frontend receives response and displays it in chat

## 🚢 Deployment

### Production Backend

```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend Deployment

The frontend is a static web application and can be deployed to:

- **Vercel**: Deploy directly from GitHub
- **Netlify**: Drag and drop the `frontend` folder
- **GitHub Pages**: Enable Pages in repository settings
- **Any web server**: Serve the `frontend` directory

### Docker Deployment (Optional)

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ ./app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🧩 Advanced Features & Extensions

### 1. Chat History Storage

Add SQLite database for persistent chat history:

```python
# Add to requirements.txt
sqlalchemy==2.0.23
alembic==1.13.1

# Create models/database.py
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True)
    role = Column(String, nullable=False)
    content = Column(String, nullable=False)
    model = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
```

### 2. RAG Integration

Add document retrieval and embedding support:

```python
# Add to requirements.txt
langchain==0.1.0
chromadb==0.4.18

# Create services/rag_service.py
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma

class RAGService:
    def __init__(self):
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        self.vectorstore = Chroma(embedding_function=self.embeddings)

    def add_documents(self, documents):
        self.vectorstore.add_documents(documents)

    def search(self, query, k=5):
        return self.vectorstore.similarity_search(query, k=k)
```

### 3. Voice Integration

Add speech-to-text and text-to-speech:

```javascript
// Add to script.js
class VoiceService {
  constructor() {
    this.recognition = new (window.SpeechRecognition ||
      window.webkitSpeechRecognition)();
    this.synthesis = window.speechSynthesis;
  }

  startListening() {
    this.recognition.start();
    this.recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      document.getElementById("chat-input").value = transcript;
    };
  }

  speak(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    this.synthesis.speak(utterance);
  }
}
```

### 4. Model Switching UI

Add a model selector dropdown:

```html
<!-- Add to index.html header -->
<select id="model-selector" class="model-selector">
  <option value="llama3">Llama 3</option>
  <option value="mistral">Mistral</option>
  <option value="codellama">Code Llama</option>
</select>
```

## 🐛 Troubleshooting

### Common Issues

**1. "Connection refused" errors**

```bash
# Check if Ollama is running
ollama list

# Start Ollama if not running
ollama serve
```

**2. CORS errors in browser**

```python
# Update allowed_origins in backend/app/core/config.py
allowed_origins: List[str] = ["*"]  # Allow all origins (development)
```

**3. Model not found**

```bash
# Download the model
ollama pull llama3

# Check available models
ollama list
```

**4. Slow responses**

```bash
# Check system resources
htop  # Linux/macOS
Task Manager  # Windows

# Consider using a smaller model
ollama pull llama3:8b  # 8B parameter version
```

### Performance Tips

- **Use GPU**: Ensure Ollama is configured to use GPU if available
- **Model Size**: Start with smaller models (7B-13B) for faster responses
- **Memory**: Ensure adequate RAM (8GB+ recommended for 7B models)
- **CPU**: More cores = faster inference on CPU-only systems

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) - For making local LLM inference accessible
- [FastAPI](https://fastapi.tiangolo.com/) - For the excellent Python web framework
- [Pydantic](https://pydantic.dev/) - For data validation and settings management

## 📞 Support

- 📖 **Documentation**: Check this README and API docs at `/docs`
- 🐛 **Issues**: Report bugs in GitHub Issues
- 💬 **Discussions**: Join GitHub Discussions for questions
- 📧 **Contact**: [Your contact information]

---

<div align="center">

**Built with ❤️ for the open-source AI community**

⭐ **Star this repo if you find it helpful!** ⭐

</div>
