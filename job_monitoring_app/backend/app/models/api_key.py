from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from .base import Base, DateMixin


class Apikey(Base, DateMixin):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    key = Column(String, unique=True)
    note = Column(String)

    expires_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="api_keys")
