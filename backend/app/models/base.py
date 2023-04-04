from sqlalchemy import text
from sqlalchemy.ext.declarative import declarative_base
from config import config

Base = declarative_base()


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
