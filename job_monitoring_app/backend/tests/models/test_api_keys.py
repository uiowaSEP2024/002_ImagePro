from app.internal.crypto import API_KEY_LENGTH

from app.services.api_keys import (
    generate_apikey,
)

from app import models, services, schemas

# TODO these will need to be refactored once we implement a required role


def test_generate_api_key():
    key = generate_apikey()

    assert isinstance(key, str)
    assert len(key) >= API_KEY_LENGTH


def test_create_api_key(db, random_test_user_no_role):
    api_key = services.create_apikey_for_user(
        db=db, user_id=random_test_user_no_role.id, key=schemas.ApikeyCreate(note="key")
    )

    assert isinstance(api_key, models.Apikey)
    assert len(api_key.key) >= API_KEY_LENGTH
    assert api_key.user_id == random_test_user_no_role.id
    assert api_key.created_at is not None

    api_keys_for_user = services.get_api_keys_for_user(db, random_test_user_no_role.id)
    assert len(api_keys_for_user) > 0
    assert api_keys_for_user[0].key == api_key.key

    user_from_api_key = services.get_user_from_apikey_key(db, api_key.key)
    assert isinstance(user_from_api_key, models.User)
    assert user_from_api_key.id == random_test_user_no_role.id


def test_get_api_keys_for_user(db, random_test_user_no_role):
    api_key1 = services.create_apikey_for_user(
        db, random_test_user_no_role.id, key=schemas.ApikeyCreate(note="key")
    )
    api_key2 = services.create_apikey_for_user(
        db, random_test_user_no_role.id, key=schemas.ApikeyCreate(note="key")
    )

    assert api_key1.user_id == random_test_user_no_role.id
    assert api_key2.user_id == random_test_user_no_role.id

    api_keys_for_user = services.get_api_keys_for_user(db, random_test_user_no_role.id)
    assert len(api_keys_for_user) == 2
    assert api_keys_for_user[0].key == api_key1.key
    assert api_keys_for_user[1].key == api_key2.key


def test_get_user_from_api_key(db, random_test_user_no_role):
    api_key = services.create_apikey_for_user(
        db, random_test_user_no_role.id, key=schemas.ApikeyCreate(note="key")
    )
    user_from_api_key = services.get_user_from_apikey_key(db, api_key.key)
    assert isinstance(user_from_api_key, models.User)
    assert user_from_api_key.id == random_test_user_no_role.id
