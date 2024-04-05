from datetime import datetime
from typing import List

from pydantic import BaseModel

from . import Event
from .study_configuration import StudyConfiguration
from .provider import Provider


class StudyBase(BaseModel):
    provider_study_id: str
    hospital_id: int


class StudyCreate(StudyBase):
    tag: str


class StudyPure(StudyBase):
    id: int
    provider_id: int
    study_configuration_id: int

    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True


class Study(StudyPure):
    provider: Provider
    study_configuration: StudyConfiguration
    events: List[Event] = []

    class Config:
        orm_mode = True
