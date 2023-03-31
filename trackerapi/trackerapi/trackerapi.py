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
