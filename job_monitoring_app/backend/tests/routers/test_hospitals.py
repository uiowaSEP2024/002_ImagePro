from app import services, schemas


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
    assert len(response.json()) == 2

    assert response.json()[0]["id"] == db_hospital_1.id
    assert response.json()[0]["hospital_name"] == db_hospital_1.hospital_name
    assert response.json()[0]["created_at"] is not None

    assert response.json()[1]["id"] == db_hospital_2.id
    assert response.json()[1]["hospital_name"] == db_hospital_2.hospital_name
    assert response.json()[1]["created_at"] is not None
