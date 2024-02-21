from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Integer, String

from .base import Base, DateMixin


class StepConfiguration(Base, DateMixin):
    """
    StepConfiguration model

    A StepConfiguration represents a specific configuration for a step.

    Attributes:
    -----------
    id : int
        Auto-generated internal job configuration id
    tag : str
        Tag used to identify a step
    name : str
        The step name as specified by the provider
    points : int
        Number of points for the step
        ?? What does this mean exactly??
        ?? What are points used for??
        ?? Why do they matter ??
        ?? Seems to be unneeded complexity ??
    job_configuration_id : int
        ForeignKey to JobConfiguration id
    job_configuration : relationship
        Relationship to the JobConfiguration model.
        Represents the job configuration associated with this step configuration
    """

    __tablename__ = "step_configurations"
    __table_args__ = (UniqueConstraint("job_configuration_id", "tag"),)

    # Auto-generated internal job configuration id
    id = Column(Integer, primary_key=True, index=True)

    # Tag used to identify a step
    tag = Column(String, index=True, nullable=False)

    # The step name as specified by the provider
    name = Column(String, index=True, nullable=False)

    # Number of points for the step
    points = Column(Integer, index=True, nullable=False)

    job_configuration_id: Column = Column(
        Integer, ForeignKey("job_configurations.id"), index=True, nullable=False
    )

    job_configuration = relationship(
        "JobConfiguration",
        back_populates="step_configurations",
        foreign_keys=[job_configuration_id],
    )

    events = relationship(
        "Event",
        back_populates="step_configuration",
        foreign_keys="Event.step_configuration_id",
    )

    metadata_configurations = relationship(
        "MetadataConfiguration",
        back_populates="step_configuration",
        foreign_keys="MetadataConfiguration.step_configuration_id",
    )
