from app import services
from app.dependencies import API_KEY_HEADER_NAME


def test_create_job(app_client, random_test_user_with_api_key):
    data = {
        "provider_job_id": "2432424",
        "customer_id": random_test_user_with_api_key.id,
        "provider_job_name": "trauma",
    }

    response = app_client.post(
        "/jobs/",
        json=data,
        headers={API_KEY_HEADER_NAME: random_test_user_with_api_key.api_keys[0].key},
    )

    assert response.status_code == 200
    assert response.json()["provider_job_name"] == "trauma"
    assert response.json()["provider_job_id"] == "2432424"
    assert response.json()["customer_id"] == random_test_user_with_api_key.id
