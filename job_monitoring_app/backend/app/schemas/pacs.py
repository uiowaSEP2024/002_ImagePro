from datetime import datetime

from pydantic import BaseModel


class PacsBase(BaseModel):
    pass


class PacsCreate(PacsBase):
    pacs_name: str
    hospital_id: int


class Pacs(PacsCreate):
    id: int
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True
