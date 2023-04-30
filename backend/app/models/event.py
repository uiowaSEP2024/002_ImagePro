from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Integer, Enum, JSON
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from .base import DateMixin, Base


class Event(Base, DateMixin):
    __tablename__ = "events"

    # Auto-generated internal event id
    id = Column(Integer, primary_key=True, index=True)

    # The job id the events correspond to
    job_id = Column(Integer, ForeignKey("jobs.id"), index=True, nullable=False)
    job = relationship("Job", back_populates="events", foreign_keys=[job_id])

    # The event_name as specified by the provider e.g. "Scanning X"
    name = Column(String, nullable=True)

    # The kind of event (info, step, error, etc.)
    kind = Column(
        Enum("step", "error", "info", "complete", name="event_kind"),
        nullable=False,
    )

    step_configuration_id = Column(
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
