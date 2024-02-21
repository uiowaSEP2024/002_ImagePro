from sqlalchemy import text, Column, DateTime
from sqlalchemy.ext.declarative import declarative_base
from backend.config import config

from sqlalchemy.sql import func

Base = declarative_base()


class DateMixin(object):
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


def truncate_all_tables():
    db = config.db.SessionLocal()
    for table in reversed(Base.metadata.sorted_tables):
        try:
            db.execute(text(f"TRUNCATE {table.name} RESTART IDENTITY CASCADE;"))
            db.commit()
        except Exception as error:
            message = f"Failed to truncate {table.name} with error: {error}. The table might not exist yet"
            print(message)
            raise AttributeError(message)
