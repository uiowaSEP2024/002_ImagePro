from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.sql.sqltypes import String, Integer
from sqlalchemy.orm import relationship

from .base import Base, DateMixin


class Study(Base, DateMixin):
    """

    Represents a study, which is a request for a computation to be performed by the system.
    Each study has steps attached to it and is created by a provider, then assigned to a hospital.

    Attributes
    ----------
    id : int
        Auto-generated internal study ID.
    provider_id : int
        ForeignKey to the User ID of the provider.
    provider_study_id : str
        The study ID as provided by the provider. This is the ID given by the provider.
        The combination of `provider_id` and `provider_study_id` is unique.
    provider_study_name : str
        The study name as specified by the provider, e.g., "ProstateV1", "KidneyV2".
        May be used to set up billing or display information later.
    hospital_id : int
        ForeignKey to the User ID of the hospital.
    study_configuration_id : int
        ForeignKey to the StudyConfiguration ID.
    events : list of Events
        A list of events associated with the study.

    """

    __tablename__ = "studies"
    __table_args__ = (UniqueConstraint("provider_id", "provider_study_id"),)

    # Auto-generated internal study id
    id: Column = Column(Integer, primary_key=True, index=True)

    provider_id: Column = Column(
        Integer, ForeignKey("users.id"), index=True, nullable=False
    )

    # The person sending the studies
    provider = relationship(
        "User", back_populates="studies", foreign_keys=[provider_id]
    )

    # The study_id as provided by the provider
    provider_study_id: Column = Column(String, index=True, nullable=False)

    # The study_name as specified by the provider e.g. ProstateV1, KidneyV2
    # May be used to set up billing or simply display information later.
    provider_study_name: Column = Column(String, index=True, nullable=True)

    # The hospital that this study belongs to. Must be a user in the system
    hospital_id: Column = Column(
        Integer, ForeignKey("users.id"), index=True, nullable=False
    )
    hospital = relationship(
        "User",
        back_populates="studies",
        foreign_keys=[
            hospital_id,
        ],
    )

    events = relationship(
        "Event",
        back_populates="study",
        foreign_keys="Event.study_id",
        cascade="all, delete-orphan",
    )

    study_configuration_id: Column = Column(
        Integer,
        ForeignKey("study_configurations.id", ondelete="SET NULL"),
        index=True,
        nullable=True,
    )

    study_configuration = relationship(
        "StudyConfiguration",
        back_populates="studies",
        # backref=backref('studies', passive_deletes=True),
        foreign_keys=[study_configuration_id],
    )
