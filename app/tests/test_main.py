from fastapi.testclient import TestClient
import pytest
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenido a la API del Bot de Cuchillos"}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_webhook_handler():
    test_message = {
        "message": {
            "text": "Hola, quisiera información sobre cuchillos",
            "from": "5551234567"
        }
    }
    response = client.post("/webhook", json=test_message)
    assert response.status_code == 200
    assert "success" in response.json()["status"] 