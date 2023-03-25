from pydantic import BaseModel


class JobBase(BaseModel):
    provider_job_id: str
    customer_id: int


class JobCreate(JobBase):
    provider_job_name: str


class Job(JobCreate):
    id: int
    provider_id: int

    class Config:
        orm_mode = True
