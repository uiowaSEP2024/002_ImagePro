from datetime import datetime
from enum import Enum
from typing import Dict, Optional, Union

from pydantic import BaseModel, Json

from .step_configuration import StepConfiguration


class EventKindEnum(str, Enum):
    step = "step"
    error = "error"
    info = "info"
    complete = "complete"


class EventBase(BaseModel):
    pass


class EventCreate(EventBase):
    name: Optional[str]
    kind: EventKindEnum
    event_metadata: Optional[Dict[str, Union[str, int, float, bool]]]


class Event(EventCreate):
    id: int
    job_id: int
    created_at: datetime = None
    updated_at: datetime = None

    step_configuration: Optional[StepConfiguration]

    class Config:
        orm_mode = True


class EventCreatePublic(EventCreate):
    provider_job_id: str
    tag: Optional[str]
