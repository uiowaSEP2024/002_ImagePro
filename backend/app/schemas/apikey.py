from pydantic import BaseModel


class ApikeyBase(BaseModel):
    key: str


class ApikeyCreate(ApikeyBase):
    pass


class Apikey(ApikeyBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
