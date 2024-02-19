from datetime import datetime
from enum import Enum
from typing import Dict, Optional, Union

from pydantic import BaseModel

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

class EventUpdate(EventCreate):
    id: int


class EventPure(EventCreate):
    id: int
    job_id: int
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True


class Event(EventPure):
    step_configuration: Optional[StepConfiguration]


class EventCreatePublic(EventCreate):
    provider_job_id: str
    tag: Optional[str]
