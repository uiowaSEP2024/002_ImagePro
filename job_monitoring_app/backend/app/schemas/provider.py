from datetime import datetime

from pydantic import BaseModel


class ProviderBase(BaseModel):
    pass


class ProviderCreate(ProviderBase):
    provider_name: str


class Provider(ProviderBase):
    id: int
    provider_name: str
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True
