from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

import json


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_create_user():
    data = {
        "email": "testuser@nofoobar.com",
        "password": "testing",
    }
    response = client.post("/users/", json=data)
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@nofoobar.com"
