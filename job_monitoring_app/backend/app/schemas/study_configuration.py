from datetime import datetime
from typing import List

from pydantic import StrictStr, StrictInt, conlist

from .pydantic_version import PydanticVersion
from .step_configuration import StepConfigurationCreate, StepConfiguration
from .unique_tag import UniqueTagModel


class StudyConfigurationBase(UniqueTagModel):
    name: StrictStr


class StudyConfigurationCreate(StudyConfigurationBase):
    version: PydanticVersion
    step_configurations: conlist(StepConfigurationCreate, unique_items=True)


class StudyConfiguration(StudyConfigurationCreate):
    id: StrictInt
    provider_id: StrictInt

    created_at: datetime = None
    updated_at: datetime = None

    step_configurations: List[StepConfiguration]

    class Config:
        orm_mode = True
        json_encoders = {PydanticVersion: lambda v: str(v)}
