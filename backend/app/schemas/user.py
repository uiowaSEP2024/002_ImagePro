from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime = None

    class Config:
        orm_mode = True
