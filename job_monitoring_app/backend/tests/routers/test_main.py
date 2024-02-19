def test_read_main(app_client):
    response = app_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
