from datetime import datetime
from typing import List

from pydantic import BaseModel

from . import Event
from .job_configuration import JobConfiguration
from .user import User


class StudyBase(BaseModel):
    provider_study_id: str
    hospital_id: int


class StudyCreate(StudyBase):
    tag: str


class StudyPure(StudyBase):
    id: int
    provider_id: int
    job_configuration_id: int

    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True


class Study(StudyPure):
    provider: User
    job_configuration: JobConfiguration
    events: List[Event] = []

    class Config:
        orm_mode = True
