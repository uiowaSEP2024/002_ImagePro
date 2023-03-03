from sqlalchemy import text
from sqlalchemy.ext.declarative import declarative_base
from app.config.database import engine, SessionLocal

Base = declarative_base()


def ensure_tables_created():
    """
    Helper method to create all tables. TODO: we should remove this once we have migrations.
    :return:
    """
    Base.metadata.create_all(bind=engine)


def truncate_all_tables():
    db = SessionLocal()
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(text(f"TRUNCATE {table.name} RESTART IDENTITY CASCADE;"))
        db.commit()
