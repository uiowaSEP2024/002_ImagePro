def test_create_user(app_client):
    data = {
        "email": "janedoe@example.com",
        "password": "abc",
        "first_name": "Jane",
        "last_name": "Doe",
    }
    response = app_client.post("/users/", json=data)
    assert response.status_code == 200
    assert response.json()["email"] == "janedoe@example.com"
    assert response.json()["created_at"] is not None


def test_read_user(app_client):
    data = {
        "email": "alexjones@example.com",
        "password": "abc",
        "first_name": "Alex",
        "last_name": "Jones",
    }
    create_user_response = app_client.post("/users/", json=data)
    created_user_id = create_user_response.json()["id"]

    read_user_response = app_client.get(f"/users/{created_user_id}")
    assert read_user_response.json()["id"] == created_user_id
    assert read_user_response.json()["created_at"] is not None
