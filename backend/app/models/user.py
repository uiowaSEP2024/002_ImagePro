from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.config.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    apikeys = relationship("Apikey", back_populates='user', cascade='all, delete-orphan')

