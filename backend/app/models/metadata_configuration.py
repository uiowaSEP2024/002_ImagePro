from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.sql.sqltypes import String, Integer
from sqlalchemy.orm import relationship

from .base import Base


class MetadataConfiguration(Base):
    __tablename__ = "metadata_configurations"
    __table_args__ = (UniqueConstraint("step_configuration_id"),)
    # Auto-generated internal metadata configuration id
    id = Column(Integer, primary_key=True, index=True)

    # name of the field specified by the provider
    field_name = Column(String, index=True, nullable=False)

    # type of the field specified by the provider
    field_type = Column(String, index=True, nullable=False)

    # value of the field specified by the provider
    field_value = Column(String, index=True, nullable=False)

    # units of the field specified by the provider
    field_units = Column(String, index=True, nullable=False)

    step_configuration_id = Column(
        Integer, ForeignKey("step_configurations.id"), index=True, nullable=False
    )

    step_configuration = relationship(
        "StepConfiguration",
        back_populates="metadata_configurations",
        foreign_keys=[step_configuration_id],
    )
