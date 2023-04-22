import requests

from .trackerapiconfig import JobConfig


class ApiUrls:
    def __init__(self, base_url):
        self.base_url = base_url

    def url(self, path):
        return f"{self.base_url}{path}"

    def events_url(self):
        return self.url("/events")

    def jobs_url(self):
        return self.url("/jobs")

    def jobs_config_url(self):
        return self.url("/jobs_configuration")


class TrackerApi:
    """
    TrackerAPI wrapper around the backend service to make requests
    to create jobs, and send events.
    """

    DEFAULT_BASE_URL = "http://localhost:8000"
    HTTP_API_KEY_HEADER_KEY = "x-api_key"

    def __init__(self, api_key, base_url=None):
        self.api_key = api_key
        self.base_url = base_url if base_url else TrackerApi.DEFAULT_BASE_URL
        self.urls = ApiUrls(self.base_url)

    def __get_headers(self):
        return {TrackerApi.HTTP_API_KEY_HEADER_KEY: self.api_key}

    @staticmethod
    def __to_json(response):
        return response.json()

    def __get(self, url):
        return self.__to_json(requests.get(url, headers=self.__get_headers()))

    def __post(self, url, data):
        return self.__to_json(
            requests.post(url, json=data, headers=self.__get_headers())
        )

    def __patch(self, url, data):
        return self.__to_json(
            requests.patch(url, json=data, headers=self.__get_headers())
        )

    def register_job(self, job_config: JobConfig):
        response = self.__post(
            self.urls.jobs_url(),
            {
                "job_config": job_config,
            },
        )
        return

    def register_and_create_job(
        self, provider_job_id, customer_id, job_config: JobConfig
    ):
        self.register_job(job_config)

        response = self.__post(
            self.urls.jobs_url(),
            {
                "provider_job_id": provider_job_id,
                "customer_id": customer_id,
                "provider_job_name": job_config.tag,
            },
        )

        return JobApi(provider_job_id=response["provider_job_id"], api=self)

    def send_event(self, kind, name, provider_job_id):
        response = self.__post(
            self.urls.events_url(),
            {"kind": kind, "name": name, "provider_job_id": provider_job_id},
    def send_event(self, kind, name, provider_job_id, metadata):
        response = self.__post_request(
            f"{self.base_url}/events",
            {"kind": kind, "name": name, "provider_job_id": provider_job_id, "event_metadata": metadata},
        )

        return EventApi(event_id=response["id"], api=self)
        return Event(event_id=response["id"], api=self)

    def send_event_metadata(self, event_id, metadata):
        response = self.__patch(
            self.urls.events_url(), {"id": event_id, "metadata": metadata}
        )

    def register_job_config(self):
        self.__post(self.urls.jobs_config_url(), {})


class JobApi:
    def __init__(self, api: TrackerApi, provider_job_id):
        self.provider_job_id = provider_job_id
        self.api = api

    def send_event(self, kind, name, metadata):
        return self.api.send_event(
            kind=kind, name=name, provider_job_id=self.provider_job_id, metadata=metadata
        )


class EventApi:
    def __init__(self, api: TrackerApi, event_id):
        self.event_id = event_id
        self.api = api

    def send_metadata(self, data):
        self.api.send_event_metadata(event_id=self.event_id, metadata={})
