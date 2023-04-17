from app import services
from app.dependencies import API_KEY_HEADER_NAME
from app import models, schemas


def test_create_event(app_client, job_for_random_user_with_api_key, db):
    job = job_for_random_user_with_api_key
    data = {
        "kind": "step",
        "name": job.provider_job_name,
        "provider_job_id": job.provider_job_id,
        # "event_metadata": {
        #     "unofficial": "Yes"
        # }
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
    # assert response.json()["event_metadata"] == {
    #     "unofficial": "Yes"
    # }
    assert response.json()["name"] == "Scanning"
    db.refresh(job)
    assert response.json()["id"] == job.events[0].id
    assert (
        response.json()["job_id"]
        == services.get_job_by_provider_job_id(
            db=db, provider_job_id=job.provider_job_id, provider_id=job.provider_id
        ).id
    )
