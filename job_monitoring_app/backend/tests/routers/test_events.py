import datetime

from app import services
from app.dependencies import API_KEY_HEADER_NAME


def test_create_event(app_client, job_for_random_user_with_api_key, db):
    job = job_for_random_user_with_api_key
    data = {
        "kind": "Pending",
        "name": "Scanning",
        "provider_job_id": job.provider_job_id,
        "event_metadata": {"official": "Yes"},
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
    assert response.json()["kind"] == "Pending"
    assert response.json()["name"] == "Scanning"
    assert response.json()["event_metadata"] == {"official": "Yes"}
    db.refresh(job)
    assert response.json()["id"] == job.events[0].id
    assert (
        response.json()["job_id"]
        == services.get_job_by_provider_job_id(
            db=db, provider_job_id=job.provider_job_id, provider_id=job.provider_id
        ).id
    )
    assert response.json()["created_at"] is not None


def test_update_event(app_client, job_for_random_user_with_api_key, db):
    # Create an event
    job = job_for_random_user_with_api_key
    event_data = {
        "kind": "Pending",
        "name": "Scanning",
        "provider_job_id": job.provider_job_id,
        "event_metadata": {"official": "Yes"},
    }
    response = app_client.post(
        "/events",
        json=event_data,
        headers={
            API_KEY_HEADER_NAME: job_for_random_user_with_api_key.provider.api_keys[
                0
            ].key
        },
    )
    assert response.status_code == 200

    # Retrieve the created event ID
    event_id = response.json()["id"]

    # Capture current time before update
    current_time_before_update = datetime.datetime.utcnow()

    # Prepare data for updating the event
    updated_event_data = {
        "kind": "Complete",
        "id": event_id,
        "event_metadata": {"Reason": "None"},
    }

    # Send update request
    update_response = app_client.post(
        "/update_event",
        json=updated_event_data,
        headers={
            API_KEY_HEADER_NAME: job_for_random_user_with_api_key.provider.api_keys[
                0
            ].key
        },
    )

    # Retrieve the updated events update time
    update_datetime = datetime.datetime.strptime(
        update_response.json()["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z"
    )
    update_datetime = update_datetime.replace(tzinfo=None)

    # Assert update was successful
    assert update_response.status_code == 200

    # Capture current time after update
    current_time_after_update = datetime.datetime.utcnow()

    # # Verify the updated event attributes

    assert update_response.json()["kind"] == updated_event_data["kind"]
    assert update_response.json()["id"] == updated_event_data["id"]
    assert (
        update_response.json()["event_metadata"] == updated_event_data["event_metadata"]
    )
    assert update_response.json()["name"] == event_data["name"]

    assert update_response.json()["job_id"] == job.id
    assert update_response.json()["created_at"] == response.json()["created_at"]

    print(current_time_before_update)
    print(update_datetime)
    print(current_time_after_update)

    assert current_time_before_update <= update_datetime <= current_time_after_update
