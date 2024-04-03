from app import services, schemas
from app.dependencies import API_KEY_HEADER_NAME


def test_create_study(
    app_client,
    random_provider_user_with_api_key,
    random_study_configuration_factory,
    random_hospital_user,
):
    study_configuration = random_study_configuration_factory.get()

    data = {
        "provider_study_id": "2432424",
        "hospital_id": random_hospital_user.id,
        "tag": study_configuration.tag,
    }

    response = app_client.post(
        "/studies",
        json=data,
        headers={
            API_KEY_HEADER_NAME: random_provider_user_with_api_key.api_keys[0].key
        },
    )

    assert response.status_code == 200
    assert response.json()["provider_study_id"] == "2432424"
    assert response.json()["hospital_id"] == random_hospital_user.id
    assert response.json()["created_at"] is not None
    assert response.json()["study_configuration_id"] == study_configuration.id


def test_get_study_as_hospital(
    app_client,
    db,
    random_provider_user_with_api_key,
    random_hospital_user,
    random_study_configuration_factory,
):
    study_configuration = random_study_configuration_factory.get()

    study = services.create_study(
        db,
        schemas.StudyCreate(
            provider_study_id="145254",
            hospital_id=random_hospital_user.id,
            tag=study_configuration.tag,
        ),
        provider=random_provider_user_with_api_key,
    )

    db.commit()
    db.refresh(study)

    # Simulate user log in
    response = app_client.post(
        "/login", data={"username": random_hospital_user.email, "password": "abc"}
    )

    # Grab access token for user
    access_token = response.json()["access_token"]

    # Use access token in the request to get a study
    response = app_client.get(
        f"/studies/{study.id}", cookies={"access_token": access_token}
    )

    assert response.status_code == 200
    assert response.json()["id"] == study.id
    assert response.json()["hospital_id"] == study.hospital_id
    assert response.json()["provider_id"] == study.provider_id
    assert response.json()["created_at"] is not None
    assert response.json()["study_configuration_id"] == study_configuration.id


def test_get_studies_as_hospital(
    app_client,
    db,
    random_provider_user_with_api_key,
    random_hospital_user,
    random_study_configuration_factory,
):
    study_configuration = random_study_configuration_factory.get()

    study1 = services.create_study(
        db,
        schemas.StudyCreate(
            provider_study_id="145254",
            hospital_id=random_hospital_user.id,
            tag=study_configuration.tag,
        ),
        provider=random_provider_user_with_api_key,
    )

    study2 = services.create_study(
        db,
        schemas.StudyCreate(
            provider_study_id="145255",
            hospital_id=random_hospital_user.id,
            tag=study_configuration.tag,
        ),
        provider=random_provider_user_with_api_key,
    )

    db.commit()
    db.refresh(study1)
    db.refresh(study2)

    # Simulate user log in
    response = app_client.post(
        "/login", data={"username": random_hospital_user.email, "password": "abc"}
    )

    # Grab access token for user
    access_token = response.json()["access_token"]

    # Use access token in the request to get a study
    response = app_client.get("/studies", cookies={"access_token": access_token})

    assert response.status_code == 200
    assert len(response.json()) == 2

    assert response.json()[0]["id"] == study1.id
    assert response.json()[0]["hospital_id"] == study1.hospital_id
    assert response.json()[0]["provider_id"] == study1.provider_id
    assert response.json()[0]["created_at"] is not None

    assert response.json()[1]["id"] == study2.id
    assert response.json()[1]["hospital_id"] == study2.hospital_id
    assert response.json()[1]["provider_id"] == study2.provider_id
    assert response.json()[1]["created_at"] is not None


def test_get_study_as_different_hospital(
    app_client,
    db,
    random_provider_user_with_api_key,
    random_test_hospital_user_factory,
    random_study_configuration_factory,
):
    hospital_a = random_test_hospital_user_factory.get()
    hospital_b = random_test_hospital_user_factory.get()

    study_configuration = random_study_configuration_factory.get()

    study = services.create_study(
        db,
        schemas.StudyCreate(
            provider_study_id="145254",
            hospital_id=hospital_a.id,
            tag=study_configuration.tag,
        ),
        provider=random_provider_user_with_api_key,
    )

    db.commit()
    db.refresh(study)

    # Simulate user log in as hospital b (different hospital from the
    # one who the study was made for)
    response = app_client.post(
        "/login", data={"username": hospital_b.email, "password": "abc"}
    )

    # Grab access token for the different hospital
    access_token = response.json()["access_token"]

    # Use access token in the request to get a study
    response = app_client.get(
        f"/studies/{study.id}", cookies={"access_token": access_token}
    )

    # Response should be rejected
    assert response.status_code == 403


def test_get_studies_as_provider(
    app_client,
    db,
    random_provider_user_with_api_key,
    random_hospital_user,
    random_study_configuration_factory,
):
    study_configuration = random_study_configuration_factory.get()

    study1 = services.create_study(
        db,
        schemas.StudyCreate(
            provider_study_id="145254",
            hospital_id=random_hospital_user.id,
            tag=study_configuration.tag,
        ),
        provider=random_provider_user_with_api_key,
    )

    study2 = services.create_study(
        db,
        schemas.StudyCreate(
            provider_study_id="145255",
            hospital_id=random_hospital_user.id,
            tag=study_configuration.tag,
        ),
        provider=random_provider_user_with_api_key,
    )

    db.commit()
    db.refresh(study1)
    db.refresh(study2)

    # Simulate user log in
    response = app_client.post(
        "/login",
        data={"username": random_provider_user_with_api_key.email, "password": "abc"},
    )

    # Grab access token for user
    access_token = response.json()["access_token"]

    # Use access token in the request to get a study
    response = app_client.get("/studies", cookies={"access_token": access_token})

    assert response.status_code == 200
    assert len(response.json()) == 2

    assert response.json()[0]["id"] == study1.id
    assert response.json()[0]["hospital_id"] == study1.hospital_id
    assert response.json()[0]["provider_id"] == study1.provider_id
    assert response.json()[0]["created_at"] is not None

    assert response.json()[1]["id"] == study2.id
    assert response.json()[1]["hospital_id"] == study2.hospital_id
    assert response.json()[1]["provider_id"] == study2.provider_id
    assert response.json()[1]["created_at"] is not None


def test_get_study_as_admin(
    app_client,
    db,
    random_provider_user_with_api_key,
    random_hospital_user,
    random_study_configuration_factory,
    random_test_admin_user,
):
    study_configuration = random_study_configuration_factory.get()

    study = services.create_study(
        db,
        schemas.StudyCreate(
            provider_study_id="145254",
            hospital_id=random_hospital_user.id,
            tag=study_configuration.tag,
        ),
        provider=random_provider_user_with_api_key,
    )

    db.commit()
    db.refresh(study)

    # Simulate user log in
    response = app_client.post(
        "/login", data={"username": random_test_admin_user.email, "password": "abc"}
    )

    # Grab access token for user
    access_token = response.json()["access_token"]

    # Use access token in the request to get a study
    response = app_client.get("/studies", cookies={"access_token": access_token})

    assert response.status_code == 200

    # Ensure that the response contains at least one study
    assert response.json()

    # Check the first study in the response
    first_study = response.json()[0]
    assert first_study["id"] == study.id
    assert first_study["hospital_id"] == study.hospital_id
    assert first_study["provider_id"] == study.provider_id
    assert first_study["created_at"] is not None

    # Ensure that study_configuration_id and study_configuration are not None
    assert "study_configuration_id" in first_study
    assert first_study["study_configuration_id"] is not None

    assert "study_configuration" in first_study
    assert first_study["study_configuration"] is not None


def test_create_study_with_missing_tag(
    app_client,
    random_provider_user_with_api_key,
    random_study_configuration_factory,
    random_hospital_user,
):
    data = {
        "provider_study_id": "2432424",
        "hospital_id": random_hospital_user.id,
    }

    response = app_client.post(
        "/studies",
        json=data,
        headers={
            API_KEY_HEADER_NAME: random_provider_user_with_api_key.api_keys[0].key
        },
    )

    assert response.status_code == 422

    assert "tag" in response.json()["detail"][0]["loc"]
    assert response.json()["detail"][0]["msg"] == "field required"
