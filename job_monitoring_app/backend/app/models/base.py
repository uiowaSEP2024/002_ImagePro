from sqlalchemy import text, Column, DateTime
from sqlalchemy.ext.declarative import declarative_base
from config import config

from sqlalchemy.sql import func

Base = declarative_base()


class DateMixin(object):
    """
    DateMixin class

    Attributes:
    -----------
    created_at : datetime
        The date and time the object was created
    updated_at : datetime
        The date and time the object was last updated

    This mixin adds the created_at and updated_at columns to the model and drys up the code
    """

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


def truncate_all_tables():
    """
    Truncates all tables in the database

    This function is used to clear the database of all data
    """
    db = config.db.SessionLocal()
    for table in reversed(Base.metadata.sorted_tables):
        try:
            db.execute(text(f"TRUNCATE {table.name} RESTART IDENTITY CASCADE;"))
            db.commit()
        except Exception as error:
            message = f"Failed to truncate {table.name} with error: {error}. The table might not exist yet"
            print(message)
            raise AttributeError(message)
