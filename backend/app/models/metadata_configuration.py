from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import String, Integer
from .base import Base


class MetadataConfiguration(Base):
    __tablename__ = "metadata_configurations"

    # Auto-generated internal metadata configuration id
    id = Column(Integer, primary_key=True, index=True)

    # internal tag used to link a job
    job_tag = Column(String, index=True, nullable=False)

    # internal tag used to link an event
    event_tag = Column(String, index=True, nullable=False)

    # name of the field specified by the provider
    provider_field_name = Column(String, index=True, nullable=False)

    # type of the field specified by the provider
    provider_field_type = Column(String, index=True, nullable=False)

    # units of the field specified by the provider
    provider_field_units = Column(String, index=True, nullable=False)
