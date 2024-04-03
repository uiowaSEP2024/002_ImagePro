from app import services, schemas, models


def test_get_hospitals(app_client, db):
    # Create hospitals

    db_hospital_1 = services.create_hospital(
        db,
        schemas.HospitalCreate(
            hospital_name="Hospital 1",
        ),
    )

    db_hospital_2 = services.create_hospital(
        db,
        schemas.HospitalCreate(
            hospital_name="Hospital 2",
        ),
    )

    db.commit()
    db.refresh(db_hospital_1)
    db.refresh(db_hospital_2)

    # Simulate get hospitals request
    response = app_client.get("/hospitals")

    assert response.status_code == 200
    assert len(response.json()) >= 2

    # Flag to check if the hospitals are found in the response
    found_hospital_1 = False
    found_hospital_2 = False

    for item in response.json():
        if item["hospital_name"] == db_hospital_1.hospital_name:
            assert item["id"] == db_hospital_1.id
            assert item["created_at"] is not None
            found_hospital_1 = True

        if item["hospital_name"] == db_hospital_2.hospital_name:
            assert item["id"] == db_hospital_2.id
            assert item["created_at"] is not None
            found_hospital_2 = True

    # Ensure both hospitals were found in the response
    assert found_hospital_1, "hospital 1 not found in response"
    assert found_hospital_2, "hospital 2 not found in response"


def test_get_hospital(db, app_client):
    hospital = models.Hospital(
        hospital_name="Test",
    )
    db.add(hospital)
    db.commit()
    response = app_client.get(f"/hospitals/{hospital.id}")
    assert response.status_code == 200
    assert response.json()["hospital_name"] == "Test"
