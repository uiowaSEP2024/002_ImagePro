from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.sql.sqltypes import String, Integer, Enum
from sqlalchemy.orm import relationship

from .base import Base


class EventConfiguration(Base):
    __tablename__ = "event_configurations"
    __table_args__ = (UniqueConstraint("tag"),)

    # Auto-generated internal job configuration id
    id = Column(Integer, primary_key=True, index=True)

    # internal tag used to link a job
    job_tag = Column(String, index=True, nullable=False)

    # internal tag used to link the configuration
    tag = Column(String, index=True, nullable=False)

    # The event configuration name as specified by the provider
    provider_event_configuration_name = Column(String, index=True, nullable=False)

    # kind of event the configuration will be created for
    kind = Column(
        Enum("step", "error", "info", "complete", name="event_configuration_kind"),
        nullable=False,
    )
