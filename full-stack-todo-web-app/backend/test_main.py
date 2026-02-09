import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_create_task_requires_auth():
    """Test that creating a task requires authentication"""
    response = client.post("/api/1/tasks", json={
        "title": "Test task",
        "description": "Test description",
        "completed": False,
        "user_id": 1
    })
    # Should return 401 or 403 since no auth token is provided
    assert response.status_code in [401, 403]

def test_get_tasks_requires_auth():
    """Test that getting tasks requires authentication"""
    response = client.get("/api/1/tasks")
    # Should return 401 since no auth token is provided
    assert response.status_code == 401