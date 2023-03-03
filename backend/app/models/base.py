from sqlalchemy.ext.declarative import declarative_base
from app.config.database import engine

Base = declarative_base()


def ensure_tables_created():
    """
    Helper method to create all tables. TODO: we should remove this once we have migrations.
    :return:
    """
    Base.metadata.create_all(bind=engine)


def ensure_tables_dropped():
    Base.metadata.drop_all(bind=engine)
