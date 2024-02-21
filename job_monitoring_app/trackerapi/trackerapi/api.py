import requests

from .schemas import JobConfig


class ApiUrls:
    def __init__(self, base_url=""):
        self.base_url = base_url

    def set_base_url(self, base_url=""):
        self.base_url = base_url

    def url(self, path):
        return f"{self.base_url}{path}"

    @property
    def events_url(self):
        return self.url("/events")

    @property
    def update_events_url(self, event_id):
        return self.url(f"/events/{event_id}")

    @property
    def jobs_url(self):
        return self.url("/jobs")

    @property
    def jobs_config_url(self):
        return self.url("/job_configurations")

    @property
    def api_key_verify_url(self):
        return self.url("/api-keys/protected")


class TrackerApi:
    """
    TrackerAPI wrapper around the backend service to make requests
    to create jobs, and send events.
    """

    DEFAULT_BASE_URL = "http://localhost:8000"
    HTTP_API_KEY_HEADER_KEY = "x-api_key"

    def __init__(self, api_key, base_url=None, skip_verify=False):
        self.api_key = api_key
        self.base_url = base_url if base_url else TrackerApi.DEFAULT_BASE_URL
        self.urls = ApiUrls(self.base_url)

        if not skip_verify:
            self.verify_api_key()

    @property
    def __headers(self):
        return {TrackerApi.HTTP_API_KEY_HEADER_KEY: self.api_key}

    @staticmethod
    def __to_json(response):
        return response.json()

    def __post(self, url, data):
        response = requests.post(url, json=data, headers=self.__headers)
        if response.status_code != 200:
            print("Response Body (non-200 status code):", response.text)
        response.raise_for_status()
        return response

    def __get(self, url):
        response = requests.get(url, headers=self.__headers)
        response.raise_for_status()
        return response

    def verify_api_key(self):
        self.__get(self.urls.api_key_verify_url)

    def register_job_config(self, config: JobConfig):
        self.__post(self.urls.jobs_config_url, config.dict())

    def create_job(self, provider_job_id: str, customer_id: int, tag: str):
        data = self.__to_json(
            self.__post(
                self.urls.jobs_url,
                {
                    "provider_job_id": provider_job_id,
                    "customer_id": customer_id,
                    "tag": tag,
                },
            )
        )

        return TrackerJobApi(provider_job_id=data["provider_job_id"], api=self)

    def send_event(self, kind, tag, provider_job_id, metadata):
        data = self.__to_json(
            self.__post(
                self.urls.events_url,
                {
                    "kind": kind,
                    "tag": tag,
                    "provider_job_id": provider_job_id,
                    "event_metadata": metadata,
                },
            )
        )

        return TrackerEventApi(event_id=data["id"], api=self)

    def update_event(self, kind, event_id, metadata):
        data = self.__to_json(
            self.__post(
                self.urls.update_events_url(event_id),
                {
                    "kind": kind,
                    "id": event_id,
                    "event_metadata": metadata,
                },
            )
        )

        return TrackerEventApi(event_id=data["id"], api=self)


class TrackerJobApi:
    def __init__(self, api: TrackerApi, provider_job_id):
        self.provider_job_id = provider_job_id
        self.api = api

    def send_event(self, kind, tag, metadata=None):
        metadata = metadata if metadata else {}
        return self.api.send_event(
            kind=kind,
            tag=tag,
            provider_job_id=self.provider_job_id,
            metadata=metadata,
        )

    def update_event(self, kind, event_id, metadata=None):
        metadata = metadata if metadata else {}
        return self.api.update_event(
            kind=kind,
            event_id=event_id,
            metadata=metadata,
        )


class TrackerEventApi:
    def __init__(self, api: TrackerApi, event_id):
        self.event_id = event_id
        self.api = api
