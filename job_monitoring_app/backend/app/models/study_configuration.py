from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.sql.sqltypes import String, Integer
from sqlalchemy.orm import relationship

from .base import Base, DateMixin


class StudyConfiguration(Base, DateMixin):
    """
    StudyConfiguration model

    A StudyConfiguration represents a specific configuration for a study. It is created by a provider and
    can be associated with multiple studies. Each StudyConfiguration is uniquely identified by a combination
    of provider_id, tag, and version.

    Attributes:
    -----------
    id : int
        Auto-generated internal study configuration id
    tag : str
        Internal tag used to link a study configuration
    name : str
        The study configuration name as specified by the provider
    provider_id : int
        ForeignKey to User id of the provider
    version : str
        Version of the study configuration
    provider : relationship
        Relationship to the User model representing the provider
    step_configurations : relationship
        Relationship to the StepConfiguration model. Represents all step configurations associated with this study configuration
    studies : relationship
        Relationship to the study model. Represents all studies associated with this study configuration
    """

    __tablename__ = "study_configurations"
    __table_args__ = (UniqueConstraint("provider_id", "tag", "version"),)

    # Auto-generated internal study configuration id
    id = Column(Integer, primary_key=True, index=True)

    # internal tag used to link a study configuration
    tag = Column(String, index=True, nullable=False)

    # The study configuration name as specified by the provider
    name = Column(String, nullable=False)

    # The provider creating the configuration
    provider_id: Column = Column(
        Integer, ForeignKey("users.id"), index=True, nullable=False
    )

    # version of the study configuration
    version = Column(String, index=True, nullable=False)

    provider = relationship(
        "User", back_populates="study_configurations", foreign_keys=[provider_id]
    )

    step_configurations = relationship(
        "StepConfiguration",
        back_populates="study_configuration",
        foreign_keys="StepConfiguration.study_configuration_id",
        cascade="all, delete-orphan",
    )

    studies = relationship(
        "Study",
        back_populates="study_configuration",
        foreign_keys="Study.study_configuration_id",
    )
