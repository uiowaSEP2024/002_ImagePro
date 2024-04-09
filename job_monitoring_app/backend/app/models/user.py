from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

from .base import Base, DateMixin


class User(Base, DateMixin):
    """
    Represents a User model.

    Attributes
    ----------
    id : int
        The primary key of the user.
    email : str
        The email of the user.
    hashed_password : str
        The hashed password of the user.
    first_name : str
        The first name of the user.
    last_name : str
        The last name of the user.
    role : str
        The role of the user (provider, hospital, admin).
    api_keys : relationship
        The API keys associated with the user (one to many).

    Notes
    -----
    Provider has many study configurations:
        A single User instance, when acting as a Provider, can be associated with multiple
        StudyConfiguration instances. This is a one-to-many relationship from the Provider's
        perspective.

    Bidirectional:
        The relationship is set up in such a way that it can be navigated in both directions.
        From a StudyConfiguration instance, you can access the associated Provider (User), and from
        a Provider (User), you can access all associated StudyConfigurations.

    Child class -> StudyConfiguration:
        Indicates that StudyConfiguration is the child class in this relationship.
        StudyConfiguration instances are the ones being "owned" or referenced by the Provider (User).

    Parent class -> Provider:
        Indicates that the User (referred to as Provider in this context) is the parent class in
        this relationship. A Provider can "own" or reference multiple StudyConfiguration instances.

    Parent-child relationship (has many to one) -> provider_study_configurations:
        Another way of saying that a Provider can have many StudyConfigurations. The
        `provider_study_configurations` seems to be the name given to this relationship, but it's not
        directly visible in the provided code.

    Child-parent relationship (one to many) -> provider (see study_configuration.py):
        Refers to the ability of a StudyConfiguration instance to reference its associated Provider (User).
        The `provider` attribute in the StudyConfiguration class is the SQLAlchemy relationship that enables this.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)

    role = Column(
        Enum("provider", "hospital", "admin", name="user_role"),
        nullable=False,
        default="hospital",
    )

    api_keys = relationship(
        "Apikey", back_populates="user", cascade="all, delete-orphan"
    )
