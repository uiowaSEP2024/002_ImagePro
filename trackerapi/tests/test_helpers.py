import os
from pathlib import Path

import pytest

from trackerapi import JobConfig, JobConfigManager, StepConfig
from trackerapi.helpers import DuplicateJobConfigException, MissingJobConfigException

test_job_config = JobConfig(name="Test Job",
                            tag="test_job",
                            steps=[StepConfig(name="Test Step", tag="test_step", points=10)]
                            )


def test_job_config_manager_init_from_configs():
    job_config_manager = JobConfigManager(
        configs=[test_job_config]
    )

    config_result = job_config_manager.get_job_config(test_job_config.tag)

    assert config_result is not None, "Expected config to be set after init"
    assert config_result.tag == "test_job", "Expected config tag to be same as provided in init"
    assert len(config_result.steps) == 1, "Expected config's steps to be present"

    assert len(job_config_manager.tags) == 1, "Expected config manager's tags length to be 1"
    assert 'test_job' in job_config_manager.tags, "Expected config's tag to be in config manager's tags"


def test_job_config_manager_init_from_config_file():
    file_dir = os.path.dirname(os.path.realpath(__file__))
    job_config_manager = JobConfigManager(
        configurations_file=Path(file_dir, "fixtures/test-job-configurations.json")
    )

    config_result = job_config_manager.get_job_config("test_schema_job")
    assert config_result is not None, "Expected config to be set after init"

    config_b_result = job_config_manager.get_job_config("test_schema_job_b")
    assert config_b_result is not None, "Expected config to be set after init"

    assert config_result.tag == "test_schema_job", "Expected config tag to be same as provided in configuration file"
    assert config_b_result.tag == "test_schema_job_b", \
        "Expected config tag to be same as provided in configuration file"

    assert len(config_result.steps) == 1, "Expected config's steps to be same as configuration file"
    assert len(config_b_result.steps) == 2, "Expected config's steps to be same as configuration file"

    assert len(job_config_manager.tags) == 2, "Expected config manager's tags length to be 2"
    assert 'test_schema_job' in job_config_manager.tags, "Expected config's tag to be in config manager's tags"
    assert 'test_schema_job_b' in job_config_manager.tags, "Expected config's tag to be in config manager's tags"


def test_job_config_manager_duplicate_job_config():
    job_config_manager = JobConfigManager(
        configs=[test_job_config]
    )

    with pytest.raises(Exception) as exc:
        job_config_manager.add_job_config(config=test_job_config)
        assert isinstance(exc, DuplicateJobConfigException)


def test_job_config_manager_missing_job_config_when_none():
    job_config_manager = JobConfigManager()

    with pytest.raises(Exception) as exc:
        job_config_manager.get_job_config(tag="test_job")
        assert isinstance(exc, MissingJobConfigException)


def test_job_config_manager_missing_job_config():
    job_config_manager = JobConfigManager(
        configs=[test_job_config]
    )

    with pytest.raises(Exception) as exc:
        job_config_manager.get_job_config(tag="unknown_job")
        assert isinstance(exc, MissingJobConfigException)
