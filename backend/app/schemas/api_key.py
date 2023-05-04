from datetime import datetime

from pydantic import BaseModel, SecretStr


class ApiKeyCreateRequest(BaseModel):
    user_id: int


class ApikeyBase(BaseModel):
    note: str


class ApikeyCreate(ApikeyBase):
    pass


class Apikey(ApikeyBase):
    id: int
    user_id: int
    key: str

    created_at: datetime = None
    updated_at: datetime = None
    expires_at: datetime = None

    class Config:
        orm_mode = True

        json_encoders = {
            SecretStr: lambda v: v.get_secret_value()[0:3] + str(v)[3:] if v else None,
        }


class ApikeyPublic(Apikey):
    key: SecretStr
