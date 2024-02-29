import pytest
from pydantic import ValidationError

from ..trackerapi import JobConfig, StepConfig, JobConfigs


def test_no_duplicate_steps():
    with pytest.raises(ValidationError) as exc:
        _ = JobConfig(
            name="Test Study",
            tag="test_study",
            step_configurations=[
                StepConfig(tag="step_1", name="Step 1", points=1),
                StepConfig(tag="step_1", name="Step 2", points=1),
            ],
            version="1.0.0",
        )
    exception: ValidationError = exc._excinfo[1]
    assert len(exception.errors()) == 1
    assert "step_configurations" in exception.errors()[0]["loc"]
    assert "value_error.list.unique_items" == exception.errors()[0]["type"]


def test_no_duplicate_studies():
    with pytest.raises(ValidationError) as exc:
        JobConfigs(
            job_configs=[
                JobConfig(
                    name="Test Study",
                    tag="test_study",
                    step_configurations=[],
                    version="1.0.0",
                ),
                JobConfig(
                    name="Test study",
                    tag="test_study",
                    step_configurations=[],
                    version="1.0.0",
                ),
            ]
        )

    exception: ValidationError = exc._excinfo[1]
    assert len(exception.errors()) == 1
    assert "job_configs" in exception.errors()[0]["loc"]
    assert "value_error.list.unique_items" == exception.errors()[0]["type"]
