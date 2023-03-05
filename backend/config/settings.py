import os
from pathlib import Path
from typing import Optional, Union

from pydantic import BaseSettings

from root import ROOT_DIR, root_path


class Settings(BaseSettings):
    project_name: str = "team03"
    project_version: str = "0.0.1"

    environment: str

    postgres_user: Optional[str] = "postgres"
    postgres_password: Optional[str] = ""
    postgres_server: Optional[str] = "localhost"
    postgres_port: Optional[str] = 5432  # default postgres port is 5432
    postgres_db: Optional[str] = ""

    algorithm: str = ""
    access_token_expire_minutes: float = 60 * 3
    secret_key: str = ""

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_server}/{self.postgres_db}"

    class Config:
        env_file = Path(ROOT_DIR) / ".env"


class ProdSettings(Settings):
    environment: str

    class Config:
        env_file = root_path(".env"), root_path(".env.prod")


class TestSettings(Settings):
    class Config:
        env_file = root_path(".env.test")


class LocalSettings(Settings):
    class Config:
        env_file = root_path(".env.local")


ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")

settings_dict = dict(
    development=LocalSettings, production=ProdSettings, test=TestSettings
)

settings_cls = settings_dict[ENVIRONMENT.lower()]

settings: Union[LocalSettings, Settings, TestSettings] = settings_cls()

print(f"Running in environment: {settings.environment}")
