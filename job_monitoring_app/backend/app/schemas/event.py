from datetime import datetime
from enum import Enum
from typing import Dict, Optional, Union

from pydantic import BaseModel

from .step_configuration import StepConfiguration


class EventKindEnum(str, Enum):
    in_progress = "In progress"
    error = "Error"
    info = "Info"
    complete = "Complete"
    pending = "Pending"


class EventBase(BaseModel):
    pass


class EventCreate(EventBase):
    name: Optional[str]
    kind: EventKindEnum
    event_metadata: Optional[Dict[str, Union[str, int, float, bool]]]


class EventPure(EventCreate):
    id: int
    study_id: int
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True


class Event(EventPure):
    step_configuration: Optional[StepConfiguration]


class EventCreatePublic(EventCreate):
    provider_study_id: str
    tag: Optional[str]


class EventUpdate(EventCreate):
    id: int
