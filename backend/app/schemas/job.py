from datetime import datetime

from pydantic import BaseModel, StrictStr


class JobBase(BaseModel):
    provider_job_id: str
    customer_id: int


class JobCreate(JobBase):
    tag: str


class Job(JobBase):
    id: int
    provider_id: int
    job_configuration_id: int

    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True
