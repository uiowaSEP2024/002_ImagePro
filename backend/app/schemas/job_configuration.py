from datetime import datetime
from typing import Optional

from pydantic import StrictStr, StrictInt, conlist

from .step_configuration import StepConfigurationCreate
from .unique_tag import UniqueTagModel


class JobConfigurationBase(UniqueTagModel):
    name: StrictStr


class JobConfigurationCreate(JobConfigurationBase):
    step_configurations: conlist(StepConfigurationCreate, unique_items=True)


class JobConfiguration(JobConfigurationCreate):
    id: StrictInt
    provider_id: StrictInt

    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True
