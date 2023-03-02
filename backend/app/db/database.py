from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def ensure_tables_created():
    """
    Helper method to create all tables. TODO: we should remove this once we have migrations.
    :return:
    """
    Base.metadata.create_all(bind=engine)


def ensure_tables_dropped():
    Base.metadata.drop_all(bind=engine)
