from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class ProviderUsers(Base):
    """
    Represents the association between users and providers.
    """

    __tablename__ = "user_provider"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    provider_id = Column(Integer, ForeignKey("providers.id", ondelete="CASCADE"))

    provider = relationship("Provider", back_populates="users")
