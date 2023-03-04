from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    api_keys = relationship(
        "Apikey", back_populates="user", cascade="all, delete-orphan"
    )
