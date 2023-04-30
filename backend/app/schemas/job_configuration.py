from datetime import datetime

from pydantic import StrictStr, StrictInt, conlist

from .pydantic_version import PydanticVersion
from .step_configuration import StepConfigurationCreate
from .unique_tag import UniqueTagModel


class JobConfigurationBase(UniqueTagModel):
    name: StrictStr


class JobConfigurationCreate(JobConfigurationBase):
    version: PydanticVersion
    step_configurations: conlist(StepConfigurationCreate, unique_items=True)


class JobConfiguration(JobConfigurationCreate):
    id: StrictInt
    provider_id: StrictInt

    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True
        json_encoders = {PydanticVersion: lambda v: str(v)}
