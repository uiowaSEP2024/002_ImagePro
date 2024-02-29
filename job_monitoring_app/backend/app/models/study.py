from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.sql.sqltypes import String, Integer
from sqlalchemy.orm import relationship

from .base import Base, DateMixin


class Study(Base, DateMixin):
    """
    A study is a request for a computation to be tracked by the system.
    ?A study is created by a provider and is assigned to a product and hospital/PACS

    Attributes:
    -----------
    id: int
        Auto-generated internal job id
    provider: int
        ForeignKey to User id of the provider
    provider_job_id: str
        The job_id as provided by the provider
        The provider_job_id and provider combo must be unique in the system
    provider_job_name: str
        The job_name as specified by the provider e.g. ProstateV1, KidneyV2
        # May be used to set up billing or simply display information later??

    hospital: int
        ForeignKey to User id of the customer
    events: list


    """

    __tablename__ = "studies"
    __table_args__ = (UniqueConstraint("provider_id", "provider_study_id"),)

    # Auto-generated internal job id
    id: Column = Column(Integer, primary_key=True, index=True)
    provider_id: Column = Column(
        Integer, ForeignKey("users.id"), index=True, nullable=False
    )
    # The person sending the jobs
    provider = relationship(
        "User", back_populates="studies", foreign_keys=[provider_id]
    )

    # The job_id as provided by the provider
    provider_study_id: Column = Column(String, index=True, nullable=False)

    # The job_name as specified by the provider e.g. ProstateV1, KidneyV2
    # May be used to set up billing or simply display information later.
    provider_study_name: Column = Column(String, index=True, nullable=True)

    # The customer that this job belongs to. Must be a user in the system
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

    job_configuration_id: Column = Column(
        Integer,
        ForeignKey("job_configurations.id", ondelete="SET NULL"),
        index=True,
        nullable=True,
    )

    job_configuration = relationship(
        "JobConfiguration",
        back_populates="studies",
        # backref=backref('jobs', passive_deletes=True),
        foreign_keys=[job_configuration_id],
    )
