from app import services
from app.dependencies import API_KEY_HEADER_NAME
from app import schemas, services


def test_create_event(app_client, job_for_random_user_with_api_key):
    job = job_for_random_user_with_api_key
    data = {
        "kind": "step",
        "name": job.provider_job_name,
        "provider_job_id": job.provider_job_id,
    }
    response = app_client.post(
        "/events",
        json=data,
        headers={
            API_KEY_HEADER_NAME: job_for_random_user_with_api_key.provider.api_keys[
                0
            ].key
        },
    )

    assert response.status_code == 200
    assert response.json()["kind"] == "step"
    assert response.json()["name"] == "Scanning"
    assert response.json()["id"] == job.id
    assert response.json()["job_id"] == job.provider_id
