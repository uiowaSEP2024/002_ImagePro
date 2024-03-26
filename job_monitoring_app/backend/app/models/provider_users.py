from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base

from .user import User
from .provider import Provider


Base = declarative_base()

# Association table
provider_user_association = Table(
    "user_provider",
    Base.metadata,
    Column(
        "user_id", Integer, ForeignKey(User.id, ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "provider_id",
        Integer,
        ForeignKey(Provider.id, ondelete="CASCADE"),
        primary_key=True,
    ),
)
