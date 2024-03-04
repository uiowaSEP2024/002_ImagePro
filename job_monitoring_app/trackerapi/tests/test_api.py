import pytest

from ..trackerapi import TrackerApi, JobConfig
import responses
import requests_mock


def test_init():
    tracker = TrackerApi(api_key="abc123", skip_verify=True)
    assert tracker.api_key == "abc123"
    assert tracker.base_url == tracker.DEFAULT_BASE_URL


def test_init_without_api_key():
    with pytest.raises(TypeError):
        _ = TrackerApi()


def test_study_requests_made_with_api_key():
    with requests_mock.Mocker() as m:
        tracker = TrackerApi(api_key="abc123", skip_verify=True)

        m.post(
            tracker.urls.studies_url,
            json={
                "provider_study_id": "1",
                "hospital_id": 1,
                "provider_study_name": "test_study",
            },
        )

        tracker.create_study("1", 1, "test_study")

        assert (
            tracker.api_key
            == m.last_request.headers[TrackerApi.HTTP_API_KEY_HEADER_KEY]
        ), "Expected api_key to be sent on request to create study"


@responses.activate
def test_study():
    tracker = TrackerApi(
        api_key="abc123", base_url=TrackerApi.DEFAULT_BASE_URL, skip_verify=True
    )

    responses.add(url=tracker.urls.jobs_config_url, method=responses.POST, json={})
    tracker.register_job_config(
        JobConfig(
            name="Test Job", tag="test_job", step_configurations=[], version="1.0.0"
        )
    )
    # TODO: make meaningful assertion about the job config once implemented

    responses.add(
        url=tracker.urls.studies_url,
        method=responses.POST,
        json={"provider_study_id": "1"},
    )

    tracker_study_api = tracker.create_study("1", 1, "test_study")
    assert (
        tracker_study_api.provider_study_id == "1"
    ), "Expected TrackerStudyApi to set the returned study_provider_id on itself"

    responses.add(url=tracker.urls.events_url, method=responses.POST, json={"id": 1})
    tracker_eventapi = tracker_study_api.send_event(kind="Pending", tag="step_1")
    assert (
        tracker_eventapi.event_id == 1
    ), "Expected TrackerEventApi to set the returned event id on itself"

    responses.add(
        url=tracker.urls.update_events_url,
        method=responses.POST,
        json={
            "kind": "Complete",
            "id": 1,
            "event_metadata": {"Reason": "None"},
        },
    )
    tracker_update_event_api = tracker_study_api.update_event(
        kind="Complete", event_id=1, metadata={"Reason": "None"}
    )
    assert (
        tracker_update_event_api.event_id == 1
    ), "Expected TrackerEventApi to set the returned event id on itself"
