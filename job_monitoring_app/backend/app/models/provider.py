from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import String, Integer
from sqlalchemy.orm import relationship

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

    relationships:
    --------------
    products: list
        A list of products that the provider owns

    # TODO Add connection to users, this should be done after users are updated
    # TODO Add connection to products when that table is created

    """

    __tablename__ = "providers"

    # Auto-generated internal provider id
    id: Column = Column(Integer, primary_key=True, index=True)

    # The name of the provider
    provider_name: Column = Column(String, index=True, nullable=False)

    products = relationship(
        "Product",
        back_populates="provider",
        foreign_keys="Product.provider_id",
        cascade="all, delete-orphan",
    )
