from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.sql.sqltypes import String, Integer
from sqlalchemy.orm import relationship

from .base import Base


class Job(Base):
    __tablename__ = "jobs"
    __table_args__ = (UniqueConstraint("provider_id", "provider_job_id"),)

    # Auto-generated internal job id
    id = Column(Integer, primary_key=True, index=True)

    # The person sending the jobs
    provider_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    provider = relationship("User", back_populates="jobs", foreign_keys=[provider_id])

    # The job_id as provided by the provider
    provider_job_id = Column(String, index=True, nullable=False)

    # The job_name as specified by the provider e.g. ProstateV1, KidneyV2
    # May be used to set up billing or simply display information later.
    provider_job_name = Column(String, index=True, nullable=False)

    # The customer that this job belongs to. Must be a user in the system
    customer_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    customer = relationship("User", back_populates="jobs", foreign_keys=[customer_id])
