import pytest

from trackerapi import TrackerApi, JobConfig
import responses
import requests_mock


def test_init():
    tracker = TrackerApi(api_key="abc123", skip_verify=True)
    assert tracker.api_key == "abc123"
    assert tracker.base_url == tracker.DEFAULT_BASE_URL


def test_init_without_api_key():
    with pytest.raises(TypeError):
        tracker = TrackerApi()


def test_requests_made_with_api_key():
    with requests_mock.Mocker() as m:
        tracker = TrackerApi(api_key="abc123", skip_verify=True)

        m.post(
            tracker.urls.jobs_url,
            json={
                "provider_job_id": "1",
                "customer_id": 1,
                "provider_job_name": "test_job",
            },
        )

        tracker.create_job("1", 1, "test_job")

        assert (
            tracker.api_key
            == m.last_request.headers[TrackerApi.HTTP_API_KEY_HEADER_KEY]
        ), "Expected api_key to be sent on request to create job"


@responses.activate
def test_job():
    tracker = TrackerApi(
        api_key="abc123", base_url=TrackerApi.DEFAULT_BASE_URL, skip_verify=True
    )

    responses.add(url=tracker.urls.jobs_config_url, method=responses.POST, json={})
    tracker.register_job_config(JobConfig(name="Test Job", tag="test_job", steps=[]))
    # TODO: make meaningful assertion about the job config once implemented

    responses.add(
        url=tracker.urls.jobs_url, method=responses.POST, json={"provider_job_id": "1"}
    )

    tracker_jobapi = tracker.create_job("1", 1, "test_job")
    assert (
        tracker_jobapi.provider_job_id == "1"
    ), "Expected TrackerJobApi to set the returned job_provider_id on itself"

    responses.add(url=tracker.urls.events_url, method=responses.POST, json={"id": 1})
    tracker_eventapi = tracker_jobapi.send_event(kind="step", name="My Event")
    assert (
        tracker_eventapi.event_id == 1
    ), "Expected TrackerEventApi to set the returned event id on itself"
