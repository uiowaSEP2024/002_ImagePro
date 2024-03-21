from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Integer
from sqlalchemy.orm import relationship

from .base import Base, DateMixin


class Product(Base, DateMixin):
    """

    Represents a product, which is a device that performs computation for a study.
    Each product is owned by a provider.


    Attributes
    ----------
    id : int
        Auto-generated internal product ID.
    product_name : str
        A name identifier given to the product.
    provider_id : int
        The ID of the provider that owns this product.

    Relationships
    -------------
    provider
        The provider that this product is connected to.

    """

    __tablename__ = "products"

    # Auto-generated internal product id
    id: Column = Column(Integer, primary_key=True, index=True)

    # A name identifier given to the product
    product_name: Column = Column(String, index=True, nullable=False)

    # The provider id that the product is connected to
    provider_id: Column = Column(
        Integer, ForeignKey("providers.id"), index=True, nullable=False
    )

    provider = relationship(
        "Provider",
        back_populates="products",
        foreign_keys=[
            provider_id,
        ],
    )
