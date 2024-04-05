from app import schemas, services
from app.dependencies import API_KEY_HEADER_NAME
from starlette import status


def create_data_dict(
    tag, name, version, step_name, points, step_tag, meta_name, units, kind
):
    return {
        "tag": tag,
        "name": name,
        "version": version,
        "step_configurations": [
            {
                "name": step_name,
                "points": points,
                "tag": step_tag,
                "metadata_configurations": [
                    {
                        "name": meta_name,
                        "units": units,
                        "kind": kind,
                    }
                ],
            }
        ],
    }


def test_create_study_configurations(app_client, random_provider_user_with_api_key):
    data = {
        "tag": "lung_cancer",
        "name": "Lung Cancer",
        "version": "1.0.0",
        "step_configurations": [],
    }

    response = app_client.post(
        "/study_configurations",
        json=data,
        headers={
            API_KEY_HEADER_NAME: random_provider_user_with_api_key.api_keys[0].key
        },
    )

    assert response.status_code == 200
    assert response.json()["tag"] == "lung_cancer"
    assert response.json()["version"] == "1.0.0"
    assert len(response.json()["step_configurations"]) == 0


def test_create_study_configurations_with_new_version(
    db, app_client, random_provider_user_with_api_key
):
    _ = services.create_study_configuration(
        db,
        provider_id=random_provider_user_with_api_key.id,
        study_configuration=schemas.StudyConfigurationCreate(
            tag="lung_cancer",
            name="Lung Cancer",
            version="1.0.0",
            step_configurations=[
                schemas.StepConfigurationCreate(
                    name="Lung Search",
                    points=10,
                    tag="lung_search",
                    metadata_configurations=[
                        schemas.MetadataConfigurationCreate(
                            name="Protein Density", units="gm/cc", kind="number"
                        )
                    ],
                )
            ],
        ),
    )

    data = create_data_dict(
        tag="lung_cancer",
        name="Lung Cancer Again",
        version="1.0.1",
        step_name="Lung Search",
        points=10,
        step_tag="lung_search",
        meta_name="Protein Density",  # Specify the unique name here
        units="gm/cc",
        kind="number",
    )

    response = app_client.post(
        "/study_configurations",
        json=data,
        headers={
            API_KEY_HEADER_NAME: random_provider_user_with_api_key.api_keys[0].key
        },
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Lung Cancer Again"
    assert response.json()["tag"] == "lung_cancer"
    assert response.json()["version"] == "1.0.1"
    assert len(response.json()["step_configurations"]) == 1
    assert (
        len(response.json()["step_configurations"][0]["metadata_configurations"]) == 1
    )


def test_create_study_configuration_with_conflicting_version(
    db, app_client, random_provider_user_with_api_key
):
    _ = services.create_study_configuration(
        db,
        provider_id=random_provider_user_with_api_key.id,
        study_configuration=schemas.StudyConfigurationCreate(
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
        "/study_configurations",
        json=data,
        headers={
            API_KEY_HEADER_NAME: random_provider_user_with_api_key.api_keys[0].key
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_study_configuration_with_conflicting_version_on_metadata(
    db, app_client, random_provider_user_with_api_key
):
    _ = services.create_study_configuration(
        db,
        provider_id=random_provider_user_with_api_key.id,
        study_configuration=schemas.StudyConfigurationCreate(
            tag="lung_cancer",
            name="Lung Cancer",
            version="1.0.0",
            step_configurations=[
                schemas.StepConfigurationCreate(
                    name="Lung Search",
                    points=10,
                    tag="lung_search",
                    metadata_configurations=[
                        schemas.MetadataConfigurationCreate(
                            name="Protein Density", units="gm/cc", kind="number"
                        )
                    ],
                )
            ],
        ),
    )

    data = create_data_dict(
        tag="lung_cancer",
        name="Lung Cancer",
        version="1.0.0",
        step_name="Lung Search",
        points=10,
        step_tag="lung_search",
        meta_name="Protein Density 2",  # Specify the unique name here
        units="gm/cc",
        kind="number",
    )

    response = app_client.post(
        "/study_configurations",
        json=data,
        headers={
            API_KEY_HEADER_NAME: random_provider_user_with_api_key.api_keys[0].key
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_study_configuration_with_same_information(
    db, app_client, random_provider_user_with_api_key
):
    original_configuration = services.create_study_configuration(
        db,
        provider_id=random_provider_user_with_api_key.id,
        study_configuration=schemas.StudyConfigurationCreate(
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
        "/study_configurations",
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


def test_get_study_configuration(
    app_client,
    db,
    random_provider_user_with_api_key,
    random_study_configuration_factory,
):
    study_configuration = random_study_configuration_factory.get()

    provider_user = services.get_user(db, study_configuration.provider.users[0].user_id)

    # Simulate user log in
    response = app_client.post(
        "/login",
        data={"username": provider_user.email, "password": "abc"},
    )

    # Grab access token for user
    access_token = response.json()["access_token"]

    # Use access token in the request to get a study
    response = app_client.get(
        f"/study_configurations/{study_configuration.id}",
        cookies={"access_token": access_token},
    )

    assert response.status_code == 200
    assert response.json()["id"] == study_configuration.id
    assert response.json()["provider_id"] == study_configuration.provider_id
    assert response.json()["created_at"] is not None
    assert response.json()["tag"] == study_configuration.tag
    assert response.json()["version"] == study_configuration.version
    assert response.json()["name"] == study_configuration.name


def test_get_study_configurations_with_specific_tag_and_version(
    app_client, db, random_provider_user_with_api_key
):
    study_configuration = services.create_study_configuration(
        db,
        provider_id=random_provider_user_with_api_key.id,
        study_configuration=schemas.StudyConfigurationCreate(
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
        f"/study_configurations/?tag={study_configuration.tag}&version={study_configuration.version}",
        cookies={"access_token": access_token},
    )

    assert response.status_code == 200
    assert response.json()[0]["id"] == study_configuration.id
    assert response.json()[0]["provider_id"] == study_configuration.provider_id
    assert response.json()[0]["created_at"] is not None
    assert response.json()[0]["tag"] == study_configuration.tag
    assert response.json()[0]["version"] == study_configuration.version
    assert response.json()[0]["name"] == study_configuration.name


def test_study_configuration_with_tag_and_latest_version(
    app_client, db, random_provider_user_with_api_key
):
    _ = (
        services.create_study_configuration(
            db,
            provider_id=random_provider_user_with_api_key.id,
            study_configuration=schemas.StudyConfigurationCreate(
                tag="lung_cancer",
                name="Lung Cancer",
                version="1.0.0",
                step_configurations=[],
            ),
        ),
    )

    study_configuration2 = services.create_study_configuration(
        db,
        provider_id=random_provider_user_with_api_key.id,
        study_configuration=schemas.StudyConfigurationCreate(
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
        f"/study_configurations/?tag={study_configuration2.tag}&version={'latest'}",
        cookies={"access_token": access_token},
    )

    assert response.status_code == 200
    assert response.json()[0]["id"] == study_configuration2.id
    assert response.json()[0]["provider_id"] == study_configuration2.provider_id
    assert response.json()[0]["created_at"] is not None
    assert response.json()[0]["tag"] == study_configuration2.tag
    assert response.json()[0]["version"] == study_configuration2.version
    assert response.json()[0]["name"] == study_configuration2.name


def test_get_all_configurations_for_tag_with_missing_version(
    app_client, db, random_provider_user_with_api_key
):
    study_configuration1 = services.create_study_configuration(
        db,
        provider_id=random_provider_user_with_api_key.id,
        study_configuration=schemas.StudyConfigurationCreate(
            tag="lung_cancer",
            name="Lung Cancer",
            version="1.0.0",
            step_configurations=[],
        ),
    )

    study_configuration2 = services.create_study_configuration(
        db,
        provider_id=random_provider_user_with_api_key.id,
        study_configuration=schemas.StudyConfigurationCreate(
            tag="lung_cancer",
            name="Lung Cancer",
            version="1.0.1",
            step_configurations=[],
        ),
    )

    study_configuration3 = services.create_study_configuration(
        db,
        provider_id=random_provider_user_with_api_key.id,
        study_configuration=schemas.StudyConfigurationCreate(
            tag="lung_cancer",
            name="Lung Cancer",
            version="1.1.1",
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
        f"/study_configurations/?tag={study_configuration1.tag}",
        cookies={"access_token": access_token},
    )

    assert response.status_code == 200
    assert len(response.json()) == 3

    assert response.json()[2]["id"] == study_configuration1.id
    assert response.json()[2]["provider_id"] == study_configuration1.provider_id
    assert response.json()[2]["created_at"] is not None
    assert response.json()[2]["tag"] == study_configuration1.tag
    assert response.json()[2]["version"] == study_configuration1.version
    assert response.json()[2]["name"] == study_configuration1.name

    assert response.json()[1]["id"] == study_configuration2.id
    assert response.json()[1]["provider_id"] == study_configuration2.provider_id
    assert response.json()[1]["created_at"] is not None
    assert response.json()[1]["tag"] == study_configuration2.tag
    assert response.json()[1]["version"] == study_configuration2.version
    assert response.json()[1]["name"] == study_configuration2.name

    assert response.json()[0]["id"] == study_configuration3.id
    assert response.json()[0]["provider_id"] == study_configuration3.provider_id
    assert response.json()[0]["created_at"] is not None
    assert response.json()[0]["tag"] == study_configuration3.tag
    assert response.json()[0]["version"] == study_configuration3.version
    assert response.json()[0]["name"] == study_configuration3.name


def test_get_list_of_latest_versions_for_all_study_configurations_with_version_latest(
    app_client, db, random_provider_user_with_api_key
):
    _ = services.create_study_configuration(
        db,
        provider_id=random_provider_user_with_api_key.id,
        study_configuration=schemas.StudyConfigurationCreate(
            tag="lung_cancer",
            name="Lung Cancer",
            version="1.0.0",
            step_configurations=[],
        ),
    )

    _ = services.create_study_configuration(
        db,
        provider_id=random_provider_user_with_api_key.id,
        study_configuration=schemas.StudyConfigurationCreate(
            tag="kidney_cancer",
            name="Kidney Cancer",
            version="1.0.0",
            step_configurations=[],
        ),
    )

    study_configuration3 = services.create_study_configuration(
        db,
        provider_id=random_provider_user_with_api_key.id,
        study_configuration=schemas.StudyConfigurationCreate(
            tag="lung_cancer",
            name="Lung Cancer",
            version="1.0.1",
            step_configurations=[],
        ),
    )

    study_configuration4 = services.create_study_configuration(
        db,
        provider_id=random_provider_user_with_api_key.id,
        study_configuration=schemas.StudyConfigurationCreate(
            tag="kidney_cancer",
            name="Kidney Cancer",
            version="1.0.2",
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
        f"/study_configurations/?version={'latest'}",
        cookies={"access_token": access_token},
    )

    assert response.status_code == 200
    assert len(response.json()) == 2

    assert response.json()[0]["id"] == study_configuration3.id
    assert response.json()[0]["provider_id"] == study_configuration3.provider_id
    assert response.json()[0]["created_at"] is not None
    assert response.json()[0]["tag"] == study_configuration3.tag
    assert response.json()[0]["version"] == study_configuration3.version
    assert response.json()[0]["name"] == study_configuration3.name

    assert response.json()[1]["id"] == study_configuration4.id
    assert response.json()[1]["provider_id"] == study_configuration4.provider_id
    assert response.json()[1]["created_at"] is not None
    assert response.json()[1]["tag"] == study_configuration4.tag
    assert response.json()[1]["version"] == study_configuration4.version
    assert response.json()[1]["name"] == study_configuration4.name


def test_get_list_of_latest_versions_for_all_study_configurations_with_empty_query_params(
    app_client, db, random_provider_user_with_api_key
):
    _ = services.create_study_configuration(
        db,
        provider_id=random_provider_user_with_api_key.id,
        study_configuration=schemas.StudyConfigurationCreate(
            tag="lung_cancer",
            name="Lung Cancer",
            version="1.0.0",
            step_configurations=[],
        ),
    )

    _ = services.create_study_configuration(
        db,
        provider_id=random_provider_user_with_api_key.id,
        study_configuration=schemas.StudyConfigurationCreate(
            tag="kidney_cancer",
            name="Kidney Cancer",
            version="1.0.0",
            step_configurations=[],
        ),
    )

    study_configuration3 = services.create_study_configuration(
        db,
        provider_id=random_provider_user_with_api_key.id,
        study_configuration=schemas.StudyConfigurationCreate(
            tag="lung_cancer",
            name="Lung Cancer",
            version="1.0.1",
            step_configurations=[],
        ),
    )

    study_configuration4 = services.create_study_configuration(
        db,
        provider_id=random_provider_user_with_api_key.id,
        study_configuration=schemas.StudyConfigurationCreate(
            tag="kidney_cancer",
            name="Kidney Cancer",
            version="1.0.2",
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
        "/study_configurations/",
        cookies={"access_token": access_token},
    )

    assert response.status_code == 200
    assert len(response.json()) == 2

    assert response.json()[0]["id"] == study_configuration3.id
    assert response.json()[0]["provider_id"] == study_configuration3.provider_id
    assert response.json()[0]["created_at"] is not None
    assert response.json()[0]["tag"] == study_configuration3.tag
    assert response.json()[0]["version"] == study_configuration3.version
    assert response.json()[0]["name"] == study_configuration3.name

    assert response.json()[1]["id"] == study_configuration4.id
    assert response.json()[1]["provider_id"] == study_configuration4.provider_id
    assert response.json()[1]["created_at"] is not None
    assert response.json()[1]["tag"] == study_configuration4.tag
    assert response.json()[1]["version"] == study_configuration4.version
    assert response.json()[1]["name"] == study_configuration4.name
