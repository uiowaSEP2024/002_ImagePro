from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.sql.sqltypes import String, Integer
from sqlalchemy.orm import relationship

from .base import Base, DateMixin


class JobConfiguration(Base, DateMixin):
    """
    JobConfiguration model

    A JobConfiguration represents a specific configuration for a job. It is created by a provider and
    can be associated with multiple jobs. Each JobConfiguration is uniquely identified by a combination
    of provider_id, tag, and version.

    Attributes:
    -----------
    id : int
        Auto-generated internal job configuration id
    tag : str
        Internal tag used to link a job configuration
    name : str
        The job configuration name as specified by the provider
    provider_id : int
        ForeignKey to User id of the provider
    version : str
        Version of the job configuration
    # TODO Figure out exactly what a relationship means in this context and add a description
    provider : relationship
        Relationship to the User model representing the provider
    step_configurations : relationship
        Relationship to the StepConfiguration model. Represents all step configurations associated with this job configuration
    jobs : relationship
        Relationship to the Job model. Represents all jobs associated with this job configuration
    """

    __tablename__ = "job_configurations"
    __table_args__ = (UniqueConstraint("provider_id", "tag", "version"),)

    # Auto-generated internal job configuration id
    id = Column(Integer, primary_key=True, index=True)

    # internal tag used to link a job configuration
    tag = Column(String, index=True, nullable=False)

    # The job configuration name as specified by the provider
    name = Column(String, nullable=False)

    # The provider creating the configuration
    provider_id: Column = Column(
        Integer, ForeignKey("users.id"), index=True, nullable=False
    )

    # version of the job configuration
    version = Column(String, index=True, nullable=False)

    provider = relationship(
        "User", back_populates="job_configurations", foreign_keys=[provider_id]
    )

    step_configurations = relationship(
        "StepConfiguration",
        back_populates="job_configuration",
        foreign_keys="StepConfiguration.job_configuration_id",
        cascade="all, delete-orphan",
    )

    jobs = relationship(
        "Job",
        back_populates="job_configuration",
        foreign_keys="Job.job_configuration_id",
    )
