from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from .base import Base, DateMixin


class Apikey(Base, DateMixin):
    """
    Apikey model

    Attributes:
    -----------
    id : int
        The primary key of the api key
    user_id : int
        The foreign key of the user
    key : str
        The api key
    note : str
        A note about the api key ??
        Seems more like a title or description
        it is required to make the api key from the frontend but not required to be unique
    expires_at : datetime
        The expiration date of the api key
    user : User
        The user that the api key belongs to
    """

    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    key = Column(String, unique=True)
    note = Column(String)

    expires_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="api_keys")
