def test_login(app_client):
    data = {
        "email": "janedoe@example.com",
        "password": "abc",
    }
    response = app_client.post("/login/", json=data)
    assert response.json() == {"token_type": "bearer"}