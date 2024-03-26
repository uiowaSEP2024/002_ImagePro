from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import String, Integer
from sqlalchemy.orm import relationship

from .base import Base, DateMixin

# from .hospital_users import hospital_user_association


class Hospital(Base, DateMixin):
    """
    A hospital is an entity that requests studies to be done by providers
    Users are either hospital users or provider users and each hospital user is connected to a hospital

    Attributes:
    -----------
    id: int
        Auto-generated internal hospital id
    hospital_name: str
        The name of the hospital


    relationships:
    --------------
    pacs: list
        A list of PACS that the hospital is connected to

    # TODO Add connection to users, this should be done after users are updated
    # TODO Add connection to PACS when that table is created

    """

    __tablename__ = "hospitals"

    # Auto-generated internal hospital id
    id: Column = Column(Integer, primary_key=True, index=True)

    # The name of the hospital
    hospital_name: Column = Column(String, index=True, nullable=False)

    pacs = relationship(
        "Pacs",
        back_populates="hospital",
        foreign_keys="Pacs.hospital_id",
        cascade="all, delete-orphan",
    )
    #
    # users = relationship(
    #     "User", secondary=hospital_user_association, back_populates="hospitals"
    # )
