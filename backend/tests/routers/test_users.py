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

    create_user_response = app_client.post(
        "/users/",
        json=data,
    )

    created_user_id = create_user_response.json()["id"]

    # Simulate user log in
    response = app_client.post(
        "/login", data={"username": data["email"], "password": data["password"]}
    )

    # Grab access token for user
    access_token = response.json()["access_token"]

    read_user_response = app_client.get(
        f"/users/{created_user_id}", cookies={"access_token": access_token}
    )

    assert read_user_response.status_code == 200
    assert read_user_response.json()["id"] == created_user_id
    assert read_user_response.json()["created_at"] is not None
