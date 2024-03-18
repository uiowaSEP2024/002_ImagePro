import pytest
from pydantic import ValidationError

from app import schemas


def test_valid_study_configuration():
    result = schemas.StudyConfigurationCreate.parse_obj(
        {
            "name": "Test Study Configuration",
            "tag": "test_study_configuration",
            "version": "1.0.0",
            "step_configurations": [],
        }
    )

    assert result is not None


def test_study_configuration_with_invalid_version():
    with pytest.raises(ValidationError) as exc:
        schemas.StudyConfigurationCreate.parse_obj(
            {
                "name": "Test Study Configuration",
                "tag": "test_study_configuration",
                "version": "1",
                "step_configurations": [],
            }
        )

    exception: ValidationError = exc._excinfo[1]
    assert len(exception.errors()) == 1
    assert "version" in exception.errors()[0]["loc"]
    assert "is not valid SemVer string" in exception.errors()[0]["msg"]
    assert exception.errors()[0]["type"] == "value_error"


def test_study_configuration_with_missing_tag():
    with pytest.raises(ValidationError) as exc:
        schemas.StudyConfigurationCreate.parse_obj(
            {
                "name": "Test Study Configuration",
                "version": "1.0.0",
                "step_configurations": [],
            }
        )

    exception: ValidationError = exc._excinfo[1]
    assert len(exception.errors()) == 1
    assert "tag" in exception.errors()[0]["loc"]
    assert exception.errors()[0]["type"] == "value_error.missing"
    assert "field required" in exception.errors()[0]["msg"]


def test_study_configuration_with_missing_name():
    with pytest.raises(ValidationError) as exc:
        schemas.StudyConfigurationCreate.parse_obj(
            {
                "tag": "test_study_configuration",
                "version": "1.0.0",
                "step_configurations": [],
            }
        )

    exception: ValidationError = exc._excinfo[1]
    assert len(exception.errors()) == 1
    assert "name" in exception.errors()[0]["loc"]
    assert exception.errors()[0]["type"] == "value_error.missing"
    assert "field required" in exception.errors()[0]["msg"]
