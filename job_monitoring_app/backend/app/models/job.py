from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.sql.sqltypes import String, Integer
from sqlalchemy.orm import relationship

from .base import Base, DateMixin


class Job(Base, DateMixin):
    """
    A job is a request for a computation to be performed by the system.
    # TODO @Zach - Can you confirm this is the correct definition? and add any additional details I may have missed?
    ?A job is created by a provider and is assigned to a customer?

    Attributes:
    -----------
    id: int
        Auto-generated internal job id
    provider: int
        ForeignKey to User id of the provider
    provider_job_id: str
        The job_id as provided by the provider
        # TODO @Zach - Can you confirm this is the correct?
        # There seems to be a unique constraint on this field that causes an error when trying to insert
        # but there is no unique constraint in the model definition which is confusing
    provider_job_name: str
        The job_name as specified by the provider e.g. ProstateV1, KidneyV2
        # May be used to set up billing or simply display information later??

    customer: int
        ForeignKey to User id of the customer
    events: list


    """

    __tablename__ = "jobs"
    __table_args__ = (UniqueConstraint("provider_id", "provider_job_id"),)

    # Auto-generated internal job id
    id: Column = Column(Integer, primary_key=True, index=True)
    provider_id: Column = Column(
        Integer, ForeignKey("users.id"), index=True, nullable=False
    )
    # The person sending the jobs
    provider = relationship("User", back_populates="jobs", foreign_keys=[provider_id])

    # The job_id as provided by the provider
    provider_job_id: Column = Column(String, index=True, nullable=False)

    # The job_name as specified by the provider e.g. ProstateV1, KidneyV2
    # May be used to set up billing or simply display information later.
    provider_job_name: Column = Column(String, index=True, nullable=True)

    # The customer that this job belongs to. Must be a user in the system
    customer_id: Column = Column(
        Integer, ForeignKey("users.id"), index=True, nullable=False
    )
    customer = relationship(
        "User",
        back_populates="jobs",
        foreign_keys=[
            customer_id,
        ],
    )

    # events = relationship(
    #     "Event",
    #     back_populates="job",
    #     foreign_keys="Event.job_id",
    #     cascade="all, delete-orphan",
    # )
    job_configuration_id: Column = Column(
        Integer,
        ForeignKey("job_configurations.id", ondelete="SET NULL"),
        index=True,
        nullable=True,
    )

    job_configuration = relationship(
        "JobConfiguration",
        back_populates="jobs",
        # backref=backref('jobs', passive_deletes=True),
        foreign_keys=[job_configuration_id],
    )
