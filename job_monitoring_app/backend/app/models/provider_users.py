from sqlalchemy import Column, Integer, ForeignKey

from .base import Base
from .user import User
from .provider import Provider


class ProviderUsers(Base):
    """
    Represents the association between users and providers.
    """

    __tablename__ = "user_provider"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"))
    provider_id = Column(Integer, ForeignKey(Provider.id, ondelete="CASCADE"))
