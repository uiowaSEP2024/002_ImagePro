from pydantic import BaseModel, Json
from typing import Any
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
    metadata: Json[Any]




class Event(EventCreate):
    id: int
    job_id: int

    class Config:
        orm_mode = True


class EventCreatePublic(EventCreate):
    provider_job_id: str
    metadata: Json[Any]
