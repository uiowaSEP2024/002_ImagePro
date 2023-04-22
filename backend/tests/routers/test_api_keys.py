from app import services
from app.dependencies import (
    API_KEY_HEADER_NAME,
    INVALID_API_KEY_CREDENTIALS_MISSING,
    INVALID_API_KEY_CREDENTIALS_UNAUTHORIZED,
)


def test_create_api_key(app_client, random_test_user):
    data = {"username": random_test_user.email, "password": "abc"}
    app_client.post("/login", data=data)
    json = {
        "note": "key-note"
    }

    response = app_client.post("/api-keys/", json=json, headers={
        "Content-Type": "application/json",
    })
    assert response.status_code == 200
    assert response.json()["user_id"] == random_test_user.id
    assert response.json()["note"] == "key-note"


def test_get_api_keys(app_client, random_test_user):
    data = {"username": random_test_user.email, "password": "abc"}
    app_client.post("/login", data=data)
    json = {
        "note": "key-note"
    }

    response = app_client.post("/api-keys/", json=json, headers={
        "Content-Type": "application/json",
    })

    response = app_client.get("/api-keys/", params=data)
    assert response.status_code == 200

    result = response.json()

    assert len(result) == 1
    assert result[0]["user_id"] == random_test_user.id
    assert result[0]["key"] is not None
    assert result[0]["note"] == "key-note"


def test_api_key_protected_route(app_client, db, random_test_user):
    api_key = services.create_apikey_for_user(db, random_test_user.id)

    response = app_client.get(
        "/api-keys/protected", headers={API_KEY_HEADER_NAME: api_key.key}
    )

    result = response.json()

    assert result == "Authorized!"


def test_missing_api_key_on_protected_route(app_client, db, random_test_user):
    api_key = services.create_apikey_for_user(db, random_test_user.id)

    response = app_client.get(
        "/api-keys/protected", headers={"bad-api-key-header": api_key.key}
    )

    result = response.json()

    assert response.status_code == 403
    assert result["detail"] == INVALID_API_KEY_CREDENTIALS_MISSING


def test_bad_api_key_on_protected_route(app_client, db, random_test_user):
    response = app_client.get(
        "/api-keys/protected", headers={API_KEY_HEADER_NAME: "key that does not exist"}
    )

    result = response.json()

    assert response.status_code == 403
    assert result["detail"] == INVALID_API_KEY_CREDENTIALS_UNAUTHORIZED
