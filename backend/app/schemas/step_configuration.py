from datetime import datetime

from pydantic import StrictStr, StrictInt

from .unique_tag import UniqueTagModel


class StepConfigurationBase(UniqueTagModel):
    name: StrictStr
    points: StrictInt


class StepConfigurationCreate(StepConfigurationBase):
    pass


class StepConfiguration(StepConfigurationBase):
    id: StrictInt
    job_configuration_id: StrictInt

    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True
