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
        Auto-generated internal study configuration id
    tag : str
        Tag used to identify a step
    name : str
        The step name as specified by the provider
    points : int
        Number of points for the step
    study_configuration_id : int
        ForeignKey to StudyConfiguration id
    study_configuration : relationship
        Relationship to the StudyConfiguration model.
        Represents the study configuration associated with this step configuration
    """

    __tablename__ = "step_configurations"
    __table_args__ = (UniqueConstraint("study_configuration_id", "tag"),)

    # Auto-generated internal study configuration id
    id = Column(Integer, primary_key=True, index=True)

    # Tag used to identify a step
    tag = Column(String, index=True, nullable=False)

    # The step name as specified by the provider
    name = Column(String, index=True, nullable=False)

    # Number of points for the step
    points = Column(Integer, index=True, nullable=False)

    study_configuration_id: Column = Column(
        Integer, ForeignKey("study_configurations.id"), index=True, nullable=False
    )

    study_configuration = relationship(
        "StudyConfiguration",
        back_populates="step_configurations",
        foreign_keys=[study_configuration_id],
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
