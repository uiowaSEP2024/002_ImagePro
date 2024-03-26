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


# for admins
class UserCreate(UserBase):
    password: str
    role: UserRoleEnum = UserRoleEnum.admin


# based on what is selected at signup, the user will be associated with hospital or provider
class UserHospitalCreate(UserBase):
    password: str
    role: UserRoleEnum = UserRoleEnum.hospital
    hospital_id: int


class UserProviderCreate(UserBase):
    password: str
    role: UserRoleEnum = UserRoleEnum.provider
    provider_id: int


class User(UserBase):
    id: int
    role: UserRoleEnum
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True
