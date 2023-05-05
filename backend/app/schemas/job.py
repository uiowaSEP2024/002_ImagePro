from datetime import datetime
from typing import List

from pydantic import BaseModel, StrictStr

from . import Event
from .job_configuration import JobConfiguration
from .user import User


class JobBase(BaseModel):
    provider_job_id: str
    customer_id: int


class JobCreate(JobBase):
    tag: str


class JobPure(JobBase):
    id: int
    provider_id: int
    job_configuration_id: int

    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True


class Job(JobPure):
    provider: User
    job_configuration: JobConfiguration
    events: List[Event] = []

    class Config:
        orm_mode = True
