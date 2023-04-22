from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.sql.sqltypes import String, Integer
from sqlalchemy.orm import relationship

from .base import Base


class JobConfiguration(Base):
    __tablename__ = "job_configurations"
    __table_args__ = (UniqueConstraint("provider_id", "tag", "version"),)

    # Auto-generated internal job configuration id
    id = Column(Integer, primary_key=True, index=True)

    # internal tag used to link a job configuration
    tag = Column(String, index=True, nullable=False)

    # The job configuration name as specified by the provider
    provider_job_configuration_name = Column(String, index=True, nullable=False)

    # The provider creating the configuration
    provider_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)

    # version of the job configuration
    version = Column(String, index=True, nullable=False)

    provider = relationship(
        "User", back_populates="provider_job_configurations", foreign_keys=[provider_id]
    )

    provider_step_configurations = relationship(
        "StepConfiguration",
        back_populates="provider_job_configuration",
    )
