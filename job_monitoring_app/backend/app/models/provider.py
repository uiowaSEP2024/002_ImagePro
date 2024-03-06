from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import String, Integer

from .base import Base, DateMixin


class Provider(Base, DateMixin):
    """
    A provider is an entity that owns products and performs studies for hospitals
    Users are either hospital users or provider users and each provider user is connected to a provider

    Attributes:
    -----------
    id: int
        Auto-generated internal provider id
    provider_name: str
        The name of the provider

    # TODO Add connection to users, this should be done after users are updated
    # TODO Add connection to products when that table is created

    """

    __tablename__ = "providers"

    # Auto-generated internal provider id
    id: Column = Column(Integer, primary_key=True, index=True)

    # The name of the provider
    provider_name: Column = Column(String, index=True, nullable=False)
