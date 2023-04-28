from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from enum import Enum


class UserRoleEnum(str, Enum):
    customer = "customer"
    provider = "provider"


class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    role: Optional[UserRoleEnum] = UserRoleEnum.customer


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True
