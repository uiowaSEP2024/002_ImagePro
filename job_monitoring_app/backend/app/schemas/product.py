from datetime import datetime

from pydantic import BaseModel


class ProductBase(BaseModel):
    pass


class ProductCreate(ProductBase):
    product_name: str
    provider_id: int


class Product(ProductCreate):
    id: int
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True
