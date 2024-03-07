from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Integer
from sqlalchemy.orm import relationship

from .base import Base, DateMixin


class Pacs(Base, DateMixin):
    """
    A PACS is a server used by hospitals to send and receive studies
    PACS communicate with products???

    #TODO @Ivan is this correct?
    Attributes:
    -----------
    id: int
        Auto-generated internal hospital id
    pacs_name: str
        A name identifier given to the PACS
    hospital_id: int
        The hospital id that the PACS is connected to


    relationships:
    --------------
    hospital:
        the hospital that this pacs is connected to
    """

    __tablename__ = "pacs"

    # Auto-generated internal PACS id
    id: Column = Column(Integer, primary_key=True, index=True)

    # A name identifier given to the PACS
    pacs_name: Column = Column(String, index=True, nullable=False)

    # The hospital id that the PACS is connected to
    hospital_id: Column = Column(
        Integer, ForeignKey("hospitals.id"), index=True, nullable=False
    )

    hospital = relationship(
        "Hospital",
        back_populates="pacs",
        foreign_keys=[
            hospital_id,
        ],
    )
