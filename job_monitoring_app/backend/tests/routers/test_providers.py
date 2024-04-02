from app import services, schemas


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
    assert len(response.json()) == 2

    assert response.json()[0]["id"] == db_provider_1.id
    assert response.json()[0]["provider_name"] == db_provider_1.provider_name
    assert response.json()[0]["created_at"] is not None

    assert response.json()[1]["id"] == db_provider_2.id
    assert response.json()[1]["provider_name"] == db_provider_2.provider_name
    assert response.json()[1]["created_at"] is not None
