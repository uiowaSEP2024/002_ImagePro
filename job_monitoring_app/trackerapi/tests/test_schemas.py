import pytest
from pydantic import ValidationError

from ..trackerapi import StudyConfig, StepConfig, StudyConfigs


def test_no_duplicate_steps():
    with pytest.raises(ValidationError) as exc:
        _ = StudyConfig(
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
        StudyConfigs(
            study_configs=[
                StudyConfig(
                    name="Test Study",
                    tag="test_study",
                    step_configurations=[],
                    version="1.0.0",
                ),
                StudyConfig(
                    name="Test Study",
                    tag="test_study",
                    step_configurations=[],
                    version="1.0.0",
                ),
            ]
        )

    exception: ValidationError = exc._excinfo[1]
    assert len(exception.errors()) == 1
    assert "study_configs" in exception.errors()[0]["loc"]
    assert "value_error.list.unique_items" == exception.errors()[0]["type"]
