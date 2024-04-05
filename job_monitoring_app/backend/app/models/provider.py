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
    study_configurations : relationship
        The study configurations associated with the user (one to many).
    studies : relationship
        The studies associated with the provider (one to many).
    users : relationship
        The users associated with the provider (one to many).

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

    # provider has many study configurations
    # bidirectional
    # Child class -> StuduyConfiguration
    # Parent class -> Provider
    # Parent-child relationship (has many to one) -> provider_study_configurations
    # Child-parent relationship (one to many) -> provider (see study_configuration.py)
    study_configurations = relationship(
        "StudyConfiguration",
        back_populates="provider",
        foreign_keys="StudyConfiguration.provider_id",
        cascade="all, delete-orphan",
    )

    studies = relationship(
        "Study",
        back_populates="provider",
        foreign_keys="Study.provider_id",
        cascade="all, delete-orphan",
    )

    users = relationship(
        "ProviderUsers",
        back_populates="provider",
        foreign_keys="ProviderUsers.provider_id",
        cascade="all, delete-orphan",
    )
