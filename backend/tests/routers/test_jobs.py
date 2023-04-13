from app import services, schemas
from app.dependencies import API_KEY_HEADER_NAME


def test_create_job(app_client, random_provider_user_with_api_key):
    data = {
        "provider_job_id": "2432424",
        "customer_id": random_provider_user_with_api_key.id,
        "provider_job_name": "trauma",
    }

    response = app_client.post(
        "/jobs",
        json=data,
        headers={
            API_KEY_HEADER_NAME: random_provider_user_with_api_key.api_keys[0].key
        },
    )

    assert response.status_code == 200
    assert response.json()["provider_job_name"] == "trauma"
    assert response.json()["provider_job_id"] == "2432424"
    assert response.json()["customer_id"] == random_provider_user_with_api_key.id


def test_get_job_as_customer(
    app_client, db, random_provider_user_with_api_key, random_test_user
):
    job = services.create_job(
        db,
        schemas.JobCreate(
            provider_job_id="145254",
            customer_id=random_test_user.id,
            provider_job_name="Scanning",
        ),
        provider=random_provider_user_with_api_key,
    )

    db.commit()
    db.refresh(job)

    # Simulate user log in
    response = app_client.post(
        "/login", data={"username": random_test_user.email, "password": "abc"}
    )

    # Grab access token for user
    access_token = response.json()["access_token"]

    # Use access token in the request to get a job
    response = app_client.get(f"/jobs/{job.id}", cookies={"access_token": access_token})

    assert response.status_code == 200
    assert response.json()["id"] == job.id
    assert response.json()["customer_id"] == job.customer_id
    assert response.json()["provider_id"] == job.provider_id
    assert response.json()["provider_job_name"] == job.provider_job_name


def test_get_jobs_as_customer(
    app_client, db, random_provider_user_with_api_key, random_test_user
):
    job1 = services.create_job(
        db,
        schemas.JobCreate(
            provider_job_id="145254",
            customer_id=random_test_user.id,
            provider_job_name="Scanning",
        ),
        provider=random_provider_user_with_api_key,
    )

    job2 = services.create_job(
        db,
        schemas.JobCreate(
            provider_job_id="145255",
            customer_id=random_test_user.id,
            provider_job_name="Scanning",
        ),
        provider=random_provider_user_with_api_key,
    )

    db.commit()
    db.refresh(job1)
    db.refresh(job2)

    # Simulate user log in
    response = app_client.post(
        "/login", data={"username": random_test_user.email, "password": "abc"}
    )

    # Grab access token for user
    access_token = response.json()["access_token"]

    # Use access token in the request to get a job
    response = app_client.get(f"/jobs", cookies={"access_token": access_token})

    assert response.status_code == 200
    assert len(response.json()) == 2

    assert response.json()[0]["id"] == job1.id
    assert response.json()[0]["customer_id"] == job1.customer_id
    assert response.json()[0]["provider_id"] == job1.provider_id
    assert response.json()[0]["provider_job_name"] == job1.provider_job_name

    assert response.json()[1]["id"] == job2.id
    assert response.json()[1]["customer_id"] == job2.customer_id
    assert response.json()[1]["provider_id"] == job2.provider_id
    assert response.json()[1]["provider_job_name"] == job2.provider_job_name


def test_get_job_as_different_customer(
    app_client, db, random_provider_user_with_api_key, random_test_user_factory
):
    customer_a = random_test_user_factory.get()
    customer_b = random_test_user_factory.get()

    job = services.create_job(
        db,
        schemas.JobCreate(
            provider_job_id="145254",
            customer_id=customer_a.id,
            provider_job_name="Scanning",
        ),
        provider=random_provider_user_with_api_key,
    )

    db.commit()
    db.refresh(job)

    # Simulate user log in as customer b (different customer from the
    # one who the job was made for)
    response = app_client.post(
        "/login", data={"username": customer_b.email, "password": "abc"}
    )

    # Grab access token for the different customer
    access_token = response.json()["access_token"]

    # Use access token in the request to get a job
    response = app_client.get(f"/jobs/{job.id}", cookies={"access_token": access_token})

    # Response should be rejected
    assert response.status_code == 403
