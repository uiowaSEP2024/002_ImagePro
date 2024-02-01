from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, StrictInt, StrictStr


class MetadataKindEnum(str, Enum):
    text = "text"
    number = "number"
    link = "link"


class MetadataConfigurationBase(BaseModel):
    name: StrictStr
    kind: MetadataKindEnum = MetadataKindEnum.text
    units: Optional[StrictStr]


class MetadataConfigurationCreate(MetadataConfigurationBase):
    pass


class MetadataConfiguration(MetadataConfigurationBase):
    id: StrictInt
    step_configuration_id: StrictInt

    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True
