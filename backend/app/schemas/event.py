from datetime import datetime

from pydantic import BaseModel, Json
from typing import Union, Dict, Optional
from enum import Enum


class EventKindEnum(str, Enum):
    step = "step"
    error = "error"
    info = "info"
    complete = "complete"


class EventBase(BaseModel):
    pass


class EventCreate(EventBase):
    kind: EventKindEnum
    name: str
    event_metadata: Optional[Dict[str, Union[str, int, float, bool]]]


class Event(EventCreate):
    id: int
    job_id: int
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True


class EventCreatePublic(EventCreate):
    provider_job_id: str
