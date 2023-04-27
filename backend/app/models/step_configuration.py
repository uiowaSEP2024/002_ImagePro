from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.sql.sqltypes import String, Integer
from sqlalchemy.orm import relationship

from .base import Base, DateMixin


class StepConfiguration(Base, DateMixin):
    __tablename__ = "step_configurations"
    __table_args__ = (UniqueConstraint("job_configuration_id", "tag"),)

    # Auto-generated internal job configuration id
    id = Column(Integer, primary_key=True, index=True)

    # internal tag used to link a step configuration
    tag = Column(String, index=True, nullable=False)

    # The step configuration name as specified by the provider
    name = Column(String, index=True, nullable=False)

    job_configuration_id = Column(
        Integer, ForeignKey("job_configurations.id"), index=True, nullable=False
    )

    job_configuration = relationship(
        "JobConfiguration",
        back_populates="step_configurations",
        foreign_keys=[job_configuration_id],
    )

    metadata_configurations = relationship(
        "MetadataConfiguration",
        back_populates="step_configuration",
    )

    # TODO: This should be linked to billing configuration in the future
    points = Column(Integer, index=True, nullable=False)
