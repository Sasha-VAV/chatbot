from fastapi.testclient import TestClient

from backend.server import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200


def test_post_root_valid_item():
    response = client.post("/", json={"name": "Alex", "age": 19})
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, Alex. You're at 19 years old"}


def test_post_root_invalid_item():
    response = client.post("/", json={"name": "alex", "age": 119})
    assert response.status_code == 422
    assert "Name must be title" in str(response.json())
    assert "Age must be between 0 and 100" in str(response.json())
