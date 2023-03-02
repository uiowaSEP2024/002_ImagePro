import os
from pathlib import Path
from typing import Optional

from pydantic import BaseSettings

from root import ROOT_DIR


class Settings(BaseSettings):
    project_name: str = "team03"
    project_version: str = "0.0.1"

    postgres_user: Optional[str] = "postgres"
    postgres_password: Optional[str] = ""
    postgres_server: Optional[str] = "localhost"
    postgres_port: Optional[str] = 5432  # default postgres port is 5432
    postgres_dbname: Optional[str] = ""

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_server}/{self.postgres_dbname}"

    class Config:
        env_file = Path(ROOT_DIR) / ".env"


settings = Settings()
