from datetime import datetime

from pydantic import BaseModel, SecretStr


class ApiKeyCreateRequest(BaseModel):
    user_id: int


class ApikeyBase(BaseModel):
    key: str


class ApikeyCreate(BaseModel):
    note: str


class Apikey(ApikeyBase):
    id: int
    user_id: int
    note: str
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True

        json_encoders = {
            SecretStr: lambda v: v.get_secret_value()[0:3] + str(v)[3:] if v else None,
        }


class ApikeyPublic(Apikey):
    key: SecretStr
