from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

from .base import Base, DateMixin


class User(Base, DateMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)

    role = Column(
        Enum("provider", "customer", name="user_role"),
        nullable=True,
        default="customer",
    )

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

    # provider has many job configurations
    # bidirectional
    # Child class -> JobConfiguration
    # Parent class -> Provider
    # Parent-child relationship (has many to one) -> provider_job_configurations
    # Child-parent relationship (one to many) -> provider (see job_configuration.py)
    job_configurations = relationship(
        "JobConfiguration",
        back_populates="provider",
        foreign_keys="JobConfiguration.provider_id",
        cascade="all, delete-orphan",
    )
