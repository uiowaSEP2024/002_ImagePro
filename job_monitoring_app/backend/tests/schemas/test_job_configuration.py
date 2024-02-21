import pytest
from pydantic import ValidationError

from ...app.schemas.job_configuration import JobConfigurationCreate


def test_valid_job_configuration():
    result = JobConfigurationCreate.parse_obj(
        {
            "name": "Test Job Configuration",
            "tag": "test_job_configuration",
            "version": "1.0.0",
            "step_configurations": [],
        }
    )

    assert result is not None


def test_job_configuration_with_invalid_version():
    with pytest.raises(ValidationError) as exc:
        JobConfigurationCreate.parse_obj(
            {
                "name": "Test Job Configuration",
                "tag": "test_job_configuration",
                "version": "1",
                "step_configurations": [],
            }
        )

    exception: ValidationError = exc._excinfo[1]
    assert len(exception.errors()) == 1
    assert "version" in exception.errors()[0]["loc"]
    assert "is not valid SemVer string" in exception.errors()[0]["msg"]
    assert exception.errors()[0]["type"] == "value_error"


def test_job_configuration_with_missing_tag():
    with pytest.raises(ValidationError) as exc:
        JobConfigurationCreate.parse_obj(
            {
                "name": "Test Job Configuration",
                "version": "1.0.0",
                "step_configurations": [],
            }
        )

    exception: ValidationError = exc._excinfo[1]
    assert len(exception.errors()) == 1
    assert "tag" in exception.errors()[0]["loc"]
    assert exception.errors()[0]["type"] == "value_error.missing"
    assert "field required" in exception.errors()[0]["msg"]


def test_job_configuration_with_missing_name():
    with pytest.raises(ValidationError) as exc:
        JobConfigurationCreate.parse_obj(
            {
                "tag": "test_job_configuration",
                "version": "1.0.0",
                "step_configurations": [],
            }
        )

    exception: ValidationError = exc._excinfo[1]
    assert len(exception.errors()) == 1
    assert "name" in exception.errors()[0]["loc"]
    assert exception.errors()[0]["type"] == "value_error.missing"
    assert "field required" in exception.errors()[0]["msg"]
