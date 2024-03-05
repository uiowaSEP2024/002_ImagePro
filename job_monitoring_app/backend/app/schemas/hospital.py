from datetime import datetime

from pydantic import BaseModel


class HospitalBase(BaseModel):
    pass


class HospitalCreate(HospitalBase):
    hospital_name: str


class Hospital(HospitalBase):
    id: int
    hospital_name: str
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True
