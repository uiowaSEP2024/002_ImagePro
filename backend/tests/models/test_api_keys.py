from app.internal.crypto import API_KEY_LENGTH

from app.services.api_keys import (
    get_user_from_api_key,
    get_api_keys_for_user,
    create_apikey_for_user,
    generate_apikey,
)

from app import models, services, schemas


def test_generate_api_key():
    key = generate_apikey()

    assert isinstance(key, str)
    assert len(key) >= API_KEY_LENGTH


def test_create_api_key(db):
    test_user = services.create_user(
        db, schemas.UserCreate(email="testuser_apikey@example.com", password="abc")
    )

    api_key = services.create_apikey_for_user(db, test_user.id)

    assert isinstance(api_key, models.Apikey)
    assert len(api_key.key) >= API_KEY_LENGTH
    assert api_key.user_id == test_user.id

    api_keys_for_user = services.get_api_keys_for_user(db, test_user.id)
    assert len(api_keys_for_user) > 0
    assert api_keys_for_user[0].key == api_key.key

    user_from_api_key = services.get_user_from_api_key(db, api_key.key)
    assert isinstance(user_from_api_key, models.User)
    assert user_from_api_key.id == test_user.id
