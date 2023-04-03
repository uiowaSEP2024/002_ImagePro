from app import models
from app.internal import get_password_hash
from config import config


def test_login(app_client):
    db = config.db.SessionLocal()
    test_user = models.User(
        email="test123@example.com",
        hashed_password=get_password_hash("abc"),
        first_name="test",
        last_name="123",
    )
    db.add(test_user)
    db.commit()

    data = {
        "username": "test123@example.com",
        "password": "abc",
    }
    response = app_client.post("/login/", data=data)
    assert response.status_code == 200
