import pytest

from trackerapi import TrackerApi


def test_init():
    trackerapi = TrackerApi(api_key="abc123")
    assert trackerapi.api_key == "abc123"
    assert trackerapi.base_url == trackerapi.DEFAULT_BASE_URL


def test_init_without_api_key():
    with pytest.raises(TypeError):
        trackerapi = TrackerApi()
