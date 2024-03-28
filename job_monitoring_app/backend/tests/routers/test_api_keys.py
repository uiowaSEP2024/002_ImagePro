from datetime import datetime
from app import services, schemas
from app.dependencies import (
    API_KEY_HEADER_NAME,
    INVALID_API_KEY_CREDENTIALS_MISSING,
    INVALID_API_KEY_CREDENTIALS_UNAUTHORIZED,
)


def test_create_api_key(app_client, random_test_admin_user):
    data = {"username": random_test_admin_user.email, "password": "abc"}
    app_client.post("/login", data=data)
    json = {"note": "key-note"}

    response = app_client.post(
        "/api-keys/",
        json=json,
        headers={
            "Content-Type": "application/json",
        },
    )
    assert response.status_code == 200
    assert response.json()["user_id"] == random_test_admin_user.id
    assert response.json()["note"] == "key-note"
    assert response.json()["created_at"] is not None


def test_create_api_key_not_authorized_provider(app_client, random_provider_user):
    data = {"username": random_provider_user.email, "password": "abc"}
    app_client.post("/login", data=data)
    json = {"note": "key-note"}

    response = app_client.post(
        "/api-keys/",
        json=json,
        headers={
            "Content-Type": "application/json",
        },
    )
    assert response.status_code == 401


def test_create_api_key_not_authorized_hospital(app_client, random_hospital_user):
    data = {"username": random_hospital_user.email, "password": "abc"}
    app_client.post("/login", data=data)
    json = {"note": "key-note"}

    response = app_client.post(
        "/api-keys/",
        json=json,
        headers={
            "Content-Type": "application/json",
        },
    )
    assert response.status_code == 401


def test_get_api_keys(app_client, random_test_admin_user):
    data = {"username": random_test_admin_user.email, "password": "abc"}
    app_client.post("/login", data=data)
    json = {"note": "key-note"}

    response = app_client.post(
        "/api-keys/",
        json=json,
        headers={
            "Content-Type": "application/json",
        },
    )

    response = app_client.get("/api-keys/", params=data)
    assert response.status_code == 200

    result = response.json()

    assert len(result) == 1
    assert result[0]["user_id"] == random_test_admin_user.id
    assert result[0]["key"] is not None
    assert result[0]["note"] == "key-note"
    assert result[0]["created_at"] is not None


def test_get_api_keys_not_authorized_provider(app_client, random_provider_user):
    data = {"username": random_provider_user.email, "password": "abc"}
    app_client.post("/login", data=data)
    json = {"note": "key-note"}

    response = app_client.post(
        "/api-keys/",
        json=json,
        headers={
            "Content-Type": "application/json",
        },
    )

    response = app_client.get("/api-keys/", params=data)
    assert response.status_code == 401


def test_get_api_keys_not_authorized_hospital(app_client, random_hospital_user):
    data = {"username": random_hospital_user.email, "password": "abc"}
    app_client.post("/login", data=data)
    json = {"note": "key-note"}

    response = app_client.post(
        "/api-keys/",
        json=json,
        headers={
            "Content-Type": "application/json",
        },
    )

    response = app_client.get("/api-keys/", params=data)
    assert response.status_code == 401


def test_api_key_protected_route(app_client, db, random_test_admin_user):
    api_key = services.create_apikey_for_user(
        db, random_test_admin_user.id, key=schemas.ApikeyCreate(note="key")
    )

    response = app_client.get(
        "/api-keys/protected", headers={API_KEY_HEADER_NAME: api_key.key}
    )

    result = response.json()

    assert result == "Authorized!"


def test_missing_api_key_on_protected_route(app_client, db, random_test_admin_user):
    api_key = services.create_apikey_for_user(
        db, random_test_admin_user.id, key=schemas.ApikeyCreate(note="key")
    )

    response = app_client.get(
        "/api-keys/protected", headers={"bad-api-key-header": api_key.key}
    )

    result = response.json()

    assert response.status_code == 403
    assert result["detail"] == INVALID_API_KEY_CREDENTIALS_MISSING


def test_bad_api_key_on_protected_route(app_client, db):
    response = app_client.get(
        "/api-keys/protected", headers={API_KEY_HEADER_NAME: "key that does not exist"}
    )

    result = response.json()

    assert response.status_code == 403
    assert result["detail"] == INVALID_API_KEY_CREDENTIALS_UNAUTHORIZED


def test_expire_api_key(db, app_client, random_test_admin_user):
    api_key = services.create_apikey_for_user(
        db, random_test_admin_user.id, key=schemas.ApikeyCreate(note="key-note")
    )

    data = {"username": random_test_admin_user.email, "password": "abc"}
    app_client.post("/login", data=data)

    app_client.post(
        f"/api-keys/{api_key.id}/expire",
        headers={
            "Content-Type": "application/json",
        },
    )

    response = app_client.get("/api-keys/", params=data)
    assert response.status_code == 200

    result = response.json()

    assert len(result) == 1
    assert result[0]["user_id"] == random_test_admin_user.id
    assert result[0]["key"] is not None
    assert result[0]["note"] == "key-note"
    assert result[0]["created_at"] is not None
    assert result[0]["expires_at"] is not None
    assert (
        datetime.fromisoformat(result[0]["expires_at"]).timestamp()
        < datetime.now().timestamp()
    )


def test_expire_already_expired_apikey(db, app_client, random_test_admin_user):
    api_key = services.create_apikey_for_user(
        db, random_test_admin_user.id, key=schemas.ApikeyCreate(note="key-note")
    )

    services.expire_apikey_for_user(db, random_test_admin_user.id, api_key.id)

    data = {"username": random_test_admin_user.email, "password": "abc"}
    app_client.post("/login", data=data)

    response = app_client.post(
        f"/api-keys/{api_key.id}/expire",
        headers={
            "Content-Type": "application/json",
        },
    )

    print(response.json())
    assert response.status_code == 400

    result = response.json()
    assert result["detail"]["msg"] == "Cannot expire already expired key"


def test_cannot_use_expired_key(db, app_client, random_test_admin_user):
    api_key = services.create_apikey_for_user(
        db, random_test_admin_user.id, key=schemas.ApikeyCreate(note="key-note")
    )

    services.expire_apikey_for_user(db, random_test_admin_user.id, api_key.id)

    response = app_client.get(
        "/api-keys/protected", headers={API_KEY_HEADER_NAME: api_key.key}
    )

    result = response.json()

    assert response.status_code == 403
    assert result["detail"] == INVALID_API_KEY_CREDENTIALS_UNAUTHORIZED
