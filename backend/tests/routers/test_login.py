from app import models
from app.internal import get_password_hash
from config.database import SessionLocal


def test_login(app_client):
    db = SessionLocal()
    test_user = models.User(
        email="test123@example.com", hashed_password=get_password_hash("abc")
    )
    db.add(test_user)
    db.commit()

    data = {
        "username": "test123@example.com",
        "password": "abc",
    }
    response = app_client.post("/login/", data=data)
    assert response.status_code == 200
