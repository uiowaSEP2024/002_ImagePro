import os
from pathlib import Path

import pytest

from ..trackerapi.schemas import StudyConfig, StepConfig
from ..trackerapi.helpers import (
    DuplicateStudyConfigException,
    MissingStudyConfigException,
    StudyConfigManager,
)

test_study_config = StudyConfig(
    name="Test Study",
    tag="test_study",
    step_configurations=[StepConfig(name="Test Step", tag="test_step", points=10)],
    version="1.0.0",
)


def test_study_config_manager_init_from_configs():
    study_config_manager = StudyConfigManager(configs=[test_study_config])

    config_result = study_config_manager.get_study_config(test_study_config.tag)

    assert config_result is not None, "Expected config to be set after init"
    assert (
        config_result.tag == "test_study"
    ), "Expected config tag to be same as provided in init"
    assert (
        len(config_result.step_configurations) == 1
    ), "Expected config's steps to be present"

    assert (
        len(study_config_manager.tags) == 1
    ), "Expected config manager's tags length to be 1"
    assert (
        "test_study" in study_config_manager.tags
    ), "Expected config's tag to be in config manager's tags"


def test_study_config_manager_init_from_config_file():
    file_dir = os.path.dirname(os.path.realpath(__file__))
    study_config_manager = StudyConfigManager(
        configurations_file=Path(file_dir, "fixtures/test-study-configurations.json")
    )

    config_result = study_config_manager.get_study_config("test_schema_study")
    assert config_result is not None, "Expected config to be set after init"

    config_b_result = study_config_manager.get_study_config("test_schema_study_b")
    assert config_b_result is not None, "Expected config to be set after init"

    assert (
        config_result.tag == "test_schema_study"
    ), "Expected config tag to be same as provided in configuration file"
    assert (
        config_b_result.tag == "test_schema_study_b"
    ), "Expected config tag to be same as provided in configuration file"

    assert (
        len(config_result.step_configurations) == 1
    ), "Expected config's step_configurations to be same as configuration file"
    assert (
        len(config_b_result.step_configurations) == 2
    ), "Expected config's step_configurations to be same as configuration file"

    assert (
        len(study_config_manager.tags) == 2
    ), "Expected config manager's tags length to be 2"
    assert (
        "test_schema_study" in study_config_manager.tags
    ), "Expected config's tag to be in config manager's tags"
    assert (
        "test_schema_study_b" in study_config_manager.tags
    ), "Expected config's tag to be in config manager's tags"


def test_study_config_manager_duplicate_study_config():
    study_config_manager = StudyConfigManager(configs=[test_study_config])

    with pytest.raises(Exception) as exc:
        study_config_manager.add_study_config(config=test_study_config)
        assert isinstance(exc, DuplicateStudyConfigException)


def test_study_config_manager_missing_study_config_when_none():
    study_config_manager = StudyConfigManager()

    with pytest.raises(Exception) as exc:
        study_config_manager.get_study_config(tag="test_study")
        assert isinstance(exc, MissingStudyConfigException)


def test_study_config_manager_missing_study_config():
    study_config_manager = StudyConfigManager(configs=[test_study_config])

    with pytest.raises(Exception) as exc:
        study_config_manager.get_study_config(tag="unknown_study")
        assert isinstance(exc, MissingStudyConfigException)
