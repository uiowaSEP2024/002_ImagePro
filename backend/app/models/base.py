import sqlalchemy
from sqlalchemy import text
from sqlalchemy.ext.declarative import declarative_base
from config.database import engine, SessionLocal

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
        try:
            db.execute(text(f"TRUNCATE {table.name} RESTART IDENTITY CASCADE;"))
            db.commit()
        except Exception as error:
            message = f"Failed to truncate {table.name} with error: {error}. The table might not exist yet"
            print(message)
            raise AttributeError(message)
