from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)

    api_keys = relationship(
        "Apikey", back_populates="user", cascade="all, delete-orphan"
    )

    jobs = relationship(
        "Job",
        back_populates="customer",
        foreign_keys="Job.customer_id",
        cascade="all, delete-orphan",
    )

    provider_jobs = relationship(
        "Job",
        back_populates="provider",
        foreign_keys="Job.provider_id",
        cascade="all, delete-orphan",
    )
