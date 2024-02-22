from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Integer, Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from .base import DateMixin, Base


class Event(Base, DateMixin):
    """
    Event model

    Attributes:
    -----------
    id : int
        The primary key of the event
    job : int
        The foreign key of the job
    event_name : str
        The name of the event
    kind : str
        The kind of event (info, step, error, etc.)
    event_metadata : dict
        The event metadata (e.g. the error message or the step number)
        ?? Are these the only two things we use to populate the event metadata ??
    """

    __tablename__ = "events"

    # Auto-generated internal event id
    id = Column(Integer, primary_key=True, index=True)

    # The job id the events correspond to
    job_id: Column = Column(Integer, ForeignKey("jobs.id"), index=True, nullable=False)
    job = relationship(
        "Job",
        back_populates="events",
        foreign_keys=[
            job_id,
        ],
    )

    # The event_name as specified by the provider e.g. "Scanning X"
    name = Column(String, nullable=True)

    # The kind of event (info, step, error, etc.)
    kind = Column(
        Enum("In progress", "Error", "Info", "Complete", "Pending", name="event_kind"),
        nullable=False,
    )
    step_configuration_id: Column = Column(
        Integer,
        ForeignKey("step_configurations.id", ondelete="SET NULL"),
        index=True,
        nullable=True,
    )
    step_configuration = relationship(
        "StepConfiguration",
        back_populates="events",
        foreign_keys=[step_configuration_id],
    )

    # The event metadata
    event_metadata = Column(JSONB)
