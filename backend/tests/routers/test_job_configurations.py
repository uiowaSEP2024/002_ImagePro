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
