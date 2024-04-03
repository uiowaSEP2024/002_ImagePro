from app import services, schemas, models


def test_get_providers(app_client, db):
    # Create providers

    db_provider_1 = services.create_provider(
        db,
        schemas.ProviderCreate(
            provider_name="Provider 1",
        ),
    )

    db_provider_2 = services.create_provider(
        db,
        schemas.ProviderCreate(
            provider_name="Provider 2",
        ),
    )

    db.commit()
    db.refresh(db_provider_1)
    db.refresh(db_provider_2)

    # Simulate get providers request
    response = app_client.get("/providers")

    assert response.status_code == 200
    assert len(response.json()) >= 2

    # Flag to check if the providers are found in the response
    found_provider_1 = False
    found_provider_2 = False

    for item in response.json():
        if item["provider_name"] == db_provider_1.provider_name:
            assert item["id"] == db_provider_1.id
            assert item["created_at"] is not None
            found_provider_1 = True

        if item["provider_name"] == db_provider_2.provider_name:
            assert item["id"] == db_provider_2.id
            assert item["created_at"] is not None
            found_provider_2 = True

    # Ensure both providers were found in the response
    assert found_provider_1, "Provider 1 not found in response"
    assert found_provider_2, "Provider 2 not found in response"


def test_get_provider(db, app_client):
    provider = models.Provider(
        provider_name="Test",
    )
    db.add(provider)
    db.commit()
    response = app_client.get(f"/providers/{provider.id}")
    assert response.status_code == 200
    assert response.json()["provider_name"] == "Test"
