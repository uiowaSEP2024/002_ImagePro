from datetime import datetime

from pydantic import BaseModel

from enum import Enum


class UserRoleEnum(str, Enum):
    hospital = "hospital"
    provider = "provider"
    admin = "admin"


class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    role: UserRoleEnum = UserRoleEnum.hospital


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True
