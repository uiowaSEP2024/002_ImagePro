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

    class Config:
        orm_mode = True
