from sqlalchemy import Column, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Integer, String

from .base import Base, DateMixin


class MetadataConfiguration(Base, DateMixin):
    __tablename__ = "metadata_configurations"
    # Auto-generated internal metadata configuration id
    id = Column(Integer, primary_key=True, index=True)

    # name of the field specified by the provider
    name = Column(String, index=True, nullable=False)

    # type of the field specified by the provider
    kind = Column(
        Enum("text", "number", "link", name="metadata_kind"),
        index=False,
        nullable=False,
        server_default="text",
    )

    # units of the field specified by the provider
    units = Column(String, index=False, nullable=True)

    step_configuration_id = Column(
        Integer, ForeignKey("step_configurations.id"), index=True, nullable=False
    )

    step_configuration = relationship(
        "StepConfiguration",
        back_populates="metadata_configurations",
        foreign_keys=[step_configuration_id],
    )
