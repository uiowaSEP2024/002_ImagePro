from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Integer
from sqlalchemy.orm import relationship

from .base import Base


class Job(Base):
    __tablename__ = "jobs"

    # Auto-generated internal job id
    id = Column(Integer, primary_key=True, index=True)

    # The job_id as provided by the client
    client_job_id = Column(String, index=True, nullable=False)

    # The job_kind as specified by the client e.g. ProstateV1, KidneyV2
    # May be used to set up billing or simply display information later.
    client_job_kind = Column(String, index=True, nullable=False)

    # The customer that this job belongs to. Must be a user in the system
    customer_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
