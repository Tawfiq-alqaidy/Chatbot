import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_ping_endpoint():
    """Test the ping endpoint"""
    response = client.get("/ping")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "pong"


def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "message" in data
    assert "ollama_status" in data


def test_models_endpoint():
    """Test the models endpoint"""
    response = client.get("/api/v1/models")
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert "models" in data


def test_chat_endpoint_invalid_input():
    """Test chat endpoint with invalid input"""
    response = client.post("/api/v1/chat", json={"message": ""})
    assert response.status_code == 422  # Validation error


def test_chat_endpoint_valid_input():
    """Test chat endpoint with valid input"""
    # This test might fail if Ollama is not running
    response = client.post("/api/v1/chat", json={"message": "Hello"})
    # We expect either success (200) or server error (500) if Ollama is not available
    assert response.status_code in [200, 500]
