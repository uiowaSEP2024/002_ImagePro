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
    # TODO this needs to be changed to 'step' instead of 'event'
    def events_url(self):
        return self.url("/events")

    @property
    # TODO this needs to be changed to 'step' instead of 'event'
    def update_events_url(self):
        return self.url("/update_event")

    @property
    def studies_url(self):
        return self.url("/studies")

    @property
    def jobs_config_url(self):
        return self.url("/job_configurations")

    @property
    def api_key_verify_url(self):
        return self.url("/api-keys/protected")


class TrackerApi:
    """
    TrackerAPI wrapper around the backend service to make requests
    to create studies, and send events.
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
        """
        Returns a JSON object with the API key as the value for the API key header
        """
        return {TrackerApi.HTTP_API_KEY_HEADER_KEY: self.api_key}

    @staticmethod
    def __to_json(response):
        return response.json()

    def __post(self, url, data):
        """
        Makes a post request to the given URL with the given data
        Returns the response
        """
        response = requests.post(url, json=data, headers=self.__headers)
        if response.status_code != 200:
            print("Response Body (non-200 status code):", response.text)
        response.raise_for_status()
        return response

    def __get(self, url):
        """
        Makes a get request to the given URL
        Returns the response
        """
        response = requests.get(url, headers=self.__headers)
        response.raise_for_status()
        return response

    def verify_api_key(self):
        """
        Makes a get request to the apikeys url
        to verify the api key, which is inserted into the headers
        """
        self.__get(self.urls.api_key_verify_url)

    def register_job_config(self, config: JobConfig):
        self.__post(self.urls.jobs_config_url, config.dict())

    def create_job(self, provider_job_id: str, customer_id: int, tag: str):
        """
        Creates a job with the given provider_job_id, customer_id, and tag
        Returns a TrackerJobApi object
        """
        data = self.__to_json(
            self.__post(
                self.urls.studies_url,
                {
                    "provider_job_id": provider_job_id,
                    "customer_id": customer_id,
                    "tag": tag,
                },
            )
        )

        return TrackerJobApi(provider_job_id=data["provider_job_id"], api=self)

    def send_event(self, kind, tag, provider_job_id, metadata):
        """
        Sends an event with the given kind, tag, provider_job_id, and metadata
        Returns a TrackerEventApi object
        """
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

    def update_event(self, kind: str, event_id: int, metadata: dict):
        """
        Updates an event with the given kind, event_id, and metadata
        Returns a TrackerEventApi object
        TODO: Kind matches to status in orthanc_data_logging.py, need to make these the same
        TODO: Need to change 'event' to 'step
        """
        data = self.__to_json(
            self.__post(
                self.urls.update_events_url,
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

    def update_event(self, kind: str, event_id: int, metadata: dict):
        """
        Updates an event with the given kind, event_id, and metadata
        Returns a TrackerEventApi object
        TODO: Kind matches to status in orthanc_data_logging.py, need to make these the same
        TODO: Need to change 'event' to 'step
        """
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
