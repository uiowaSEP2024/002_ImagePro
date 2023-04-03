import requests


class TrackerAPI:
    """
    TrackerAPI wrapper around the backend service to make requests
    to create jobs, and send events.
    """

    DEFAULT_BASE_URL = "http://localhost:8000"

    def __init__(self, api_key, base_url=None):
        self.api_key = api_key
        self.base_url = base_url if base_url else TrackerAPI.DEFAULT_BASE_URL

    def __get_headers(self):
        return {"x-api_key": self.api_key}

    @staticmethod
    def __to_json(response):
        return response.json()

    def __get_request(self, url):
        return self.__to_json(requests.get(url, headers=self.__get_headers()))

    def __post_request(self, url, data):
        return self.__to_json(
            requests.post(url, json=data, headers=self.__get_headers())
        )

    def __patch_request(self, url, data):
        return self.__to_json(
            requests.patch(url, json=data, headers=self.__get_headers())
        )

    def create_job(self, id=None, customer_id=None, job_name=None):
        response = self.__post_request(
            "http://localhost:8000/jobs",
            {
                "provider_job_id": id,
                "customer_id": customer_id,
                "provider_job_name": job_name,
            },
        )
        return Job(provider_job_id=id, api=self)


class Job:
    def __init__(self, api: TrackerAPI, provider_job_id=None):
        self.provider_job_id = provider_job_id
        self.api = api

    def send_event(self, kind=None, name=None):
        return self.api.send_event(
            kind=kind, name=name, provider_job_id=self.provider_job_id
        )


class Event:
    def __init__(self, api: TrackerAPI, event_id=None):
        self.event_id = event_id
        self.api = api

    def send_metadata(self, data=None):
        self.api.send_event_metadata(event_id=self.event_id, metadata={})
