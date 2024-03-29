from app.schemas.user import UserRoleEnum
from app.schemas.hospital import HospitalCreate
from app.schemas.provider import ProviderCreate
from app.services.hospitals import create_hospital
from app.services.providers import create_provider


def test_create_user_no_role(app_client):
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


def test_create_user_provider_role(db, app_client):

    # Create a test provider
    provider = create_provider(
        db,
        ProviderCreate(
            provider_name="Test Provider",
        ),
    )

    data = {
        "email": "p@example.com",
        "password": "abc",
        "first_name": "Paul",
        "last_name": "Doe",
        "role": UserRoleEnum.provider,
        "provider_id": provider.id,
    }
    response = app_client.post("/users/", json=data)
    assert response.status_code == 200
    assert response.json()["email"] == "p@example.com"
    assert response.json()["role"] == UserRoleEnum.provider
    assert response.json()["created_at"] is not None


def test_create_user_hospital_role(db, app_client):

    # Create a test hospital
    hospital = create_hospital(
        db,
        HospitalCreate(
            hospital_name="Test Hospital",
        ),
    )

    data = {
        "email": "gh@example.com",
        "password": "abc",
        "first_name": "Jess",
        "last_name": "Doe",
        "role": UserRoleEnum.hospital,
        "hospital_id": hospital.id,
    }
    response = app_client.post("/users/", json=data)
    assert response.status_code == 200
    assert response.json()["email"] == "gh@example.com"
    assert response.json()["role"] == UserRoleEnum.hospital
    assert response.json()["created_at"] is not None


def test_create_user_admin_role(app_client):
    data = {
        "email": "ui@example.com",
        "password": "abc",
        "first_name": "Will",
        "last_name": "Doe",
        "role": UserRoleEnum.admin,
    }
    response = app_client.post("/users/", json=data)
    assert response.status_code == 200
    assert response.json()["email"] == "ui@example.com"
    assert response.json()["role"] == UserRoleEnum.admin
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
