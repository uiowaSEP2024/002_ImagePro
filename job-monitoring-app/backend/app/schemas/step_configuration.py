from datetime import datetime
from typing import List, Optional

from pydantic import StrictInt, StrictStr

from .metadata_configuration import MetadataConfiguration, MetadataConfigurationCreate
from .unique_tag import UniqueTagModel


class StepConfigurationBase(UniqueTagModel):
    name: StrictStr
    points: StrictInt


class StepConfigurationCreate(StepConfigurationBase):
    metadata_configurations: Optional[List[MetadataConfigurationCreate]] = []


class StepConfiguration(StepConfigurationBase):
    id: StrictInt
    job_configuration_id: StrictInt

    metadata_configurations: Optional[List[MetadataConfiguration]]

    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True
