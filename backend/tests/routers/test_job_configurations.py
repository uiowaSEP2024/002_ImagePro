from starlette import status

from app import services, schemas
from app.dependencies import API_KEY_HEADER_NAME


def test_create_job_configurations(app_client, random_provider_user_with_api_key):
    data = {
        "tag": "lung_cancer",
        "name": "Lung Cancer",
        "version": "1.0.0",
        "step_configurations": [],
    }

    response = app_client.post(
        "/job_configurations",
        json=data,
        headers={
            API_KEY_HEADER_NAME: random_provider_user_with_api_key.api_keys[0].key
        },
    )

    assert response.status_code == 200
    assert response.json()["tag"] == "lung_cancer"
    assert response.json()["version"] == "1.0.0"
    assert len(response.json()["step_configurations"]) == 0


def test_create_job_configurations_with_new_version(
    db, app_client, random_provider_user_with_api_key
):
    services.create_job_configuration(
        db,
        provider_id=random_provider_user_with_api_key.id,
        job_configuration=schemas.JobConfigurationCreate(
            tag="lung_cancer",
            name="Lung Cancer",
            version="1.0.0",
            step_configurations=[],
        ),
    )

    data = {
        "tag": "lung_cancer",
        "name": "Lung Cancer Again",
        "version": "1.0.1",
        "step_configurations": [],
    }

    response = app_client.post(
        "/job_configurations",
        json=data,
        headers={
            API_KEY_HEADER_NAME: random_provider_user_with_api_key.api_keys[0].key
        },
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Lung Cancer Again"
    assert response.json()["tag"] == "lung_cancer"
    assert response.json()["version"] == "1.0.1"
    assert len(response.json()["step_configurations"]) == 0


def test_create_job_configuration_with_conflicting_version(
    db, app_client, random_provider_user_with_api_key
):
    result = services.create_job_configuration(
        db,
        provider_id=random_provider_user_with_api_key.id,
        job_configuration=schemas.JobConfigurationCreate(
            tag="lung_cancer",
            name="Lung Cancer",
            version="1.0.0",
            step_configurations=[],
        ),
    )

    data = {
        "tag": "lung_cancer",
        "name": "Lung Cancer Again",  # New field but same version + tag
        "version": "1.0.0",
        "step_configurations": [],
    }

    response = app_client.post(
        "/job_configurations",
        json=data,
        headers={
            API_KEY_HEADER_NAME: random_provider_user_with_api_key.api_keys[0].key
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_job_configuration_with_same_information(
    db, app_client, random_provider_user_with_api_key
):
    original_configuration = services.create_job_configuration(
        db,
        provider_id=random_provider_user_with_api_key.id,
        job_configuration=schemas.JobConfigurationCreate(
            tag="lung_cancer",
            name="Lung Cancer",
            version="1.0.0",
            step_configurations=[],
        ),
    )

    data = {
        "tag": "lung_cancer",
        "name": "Lung Cancer",
        "version": "1.0.0",
        "step_configurations": [],
    }

    response = app_client.post(
        "/job_configurations",
        json=data,
        headers={
            API_KEY_HEADER_NAME: random_provider_user_with_api_key.api_keys[0].key
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["tag"] == original_configuration.tag
    assert response.json()["version"] == original_configuration.version
    assert response.json()["name"] == original_configuration.name
    assert (
        response.json()["step_configurations"]
        == original_configuration.step_configurations
    )


def test_get_job_configuration(
    app_client,
    db,
    random_provider_user_with_api_key,
    random_job_configuration_factory,
):
    job_configuration = random_job_configuration_factory.get()

    # Simulate user log in
    response = app_client.post(
        "/login",
        data={"username": random_provider_user_with_api_key.email, "password": "abc"},
    )

    # Grab access token for user
    access_token = response.json()["access_token"]

    # Use access token in the request to get a job
    response = app_client.get(
        f"/job_configurations/{job_configuration.id}",
        cookies={"access_token": access_token},
    )

    assert response.status_code == 200
    assert response.json()["id"] == job_configuration.id
    assert response.json()["provider_id"] == job_configuration.provider_id
    assert response.json()["created_at"] is not None
    assert response.json()["tag"] == job_configuration.tag
    assert response.json()["version"] == job_configuration.version
    assert response.json()["name"] == job_configuration.name


def test_get_job_configurations_with_specific_tag_and_version(
    app_client, db, random_provider_user_with_api_key
):
    job_configuration = services.create_job_configuration(
        db,
        provider_id=random_provider_user_with_api_key.id,
        job_configuration=schemas.JobConfigurationCreate(
            tag="lung_cancer",
            name="Lung Cancer",
            version="1.0.0",
            step_configurations=[],
        ),
    )

    # Simulate user log in
    response = app_client.post(
        "/login",
        data={"username": random_provider_user_with_api_key.email, "password": "abc"},
    )

    # Grab access token for user
    access_token = response.json()["access_token"]

    response = app_client.get(
        f"/job_configurations/?tag={job_configuration.tag}&version={job_configuration.version}",
        cookies={"access_token": access_token},
    )

    assert response.json()[0]["id"] == job_configuration.id
    assert response.json()[0]["provider_id"] == job_configuration.provider_id
    assert response.json()[0]["created_at"] is not None
    assert response.json()[0]["tag"] == job_configuration.tag
    assert response.json()[0]["version"] == job_configuration.version
    assert response.json()[0]["name"] == job_configuration.name


def test_job_configuration_with_tag_and_latest_version(
    app_client, db, random_provider_user_with_api_key
):
    job_configuration1 = (
        services.create_job_configuration(
            db,
            provider_id=random_provider_user_with_api_key.id,
            job_configuration=schemas.JobConfigurationCreate(
                tag="lung_cancer",
                name="Lung Cancer",
                version="1.0.0",
                step_configurations=[],
            ),
        ),
    )

    job_configuration2 = services.create_job_configuration(
        db,
        provider_id=random_provider_user_with_api_key.id,
        job_configuration=schemas.JobConfigurationCreate(
            tag="lung_cancer",
            name="Lung Cancer",
            version="1.0.1",
            step_configurations=[],
        ),
    )

    # Simulate user log in
    response = app_client.post(
        "/login",
        data={"username": random_provider_user_with_api_key.email, "password": "abc"},
    )

    # Grab access token for user
    access_token = response.json()["access_token"]

    response = app_client.get(
        f"/job_configurations/?tag={job_configuration2.tag}&version={'latest'}",
        cookies={"access_token": access_token},
    )

    assert response.json()[0]["id"] == job_configuration2.id
    assert response.json()[0]["provider_id"] == job_configuration2.provider_id
    assert response.json()[0]["created_at"] is not None
    assert response.json()[0]["tag"] == job_configuration2.tag
    assert response.json()[0]["version"] == job_configuration2.version
    assert response.json()[0]["name"] == job_configuration2.name
