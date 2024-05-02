from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Database:
    def __init__(self, database_url: str = None):
        self.engine = create_engine(
            database_url,
            pool_size=10,  # Increase pool size from default
            max_overflow=20,  # Increase max overflow
            pool_timeout=60,  # Increase timeout to 60 seconds
        )
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
