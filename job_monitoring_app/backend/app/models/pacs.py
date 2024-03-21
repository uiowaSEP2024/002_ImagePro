from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Integer
from sqlalchemy.orm import relationship

from .base import Base, DateMixin


class Pacs(Base, DateMixin):
    """

    Represents a PACS (Picture Archiving and Communication System) server used by hospitals to send and receive studies. PACS communicate with various medical imaging products.


    Attributes
    ----------
    id : int
        Auto-generated internal ID for the PACS.
    pacs_name : str
        A name identifier given to the PACS.
    hospital_id : int
        The ID of the hospital that the PACS is connected to.

    Relationships
    -------------
    hospital : list
        A list of hospital instances that the PACS is connected to.

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
