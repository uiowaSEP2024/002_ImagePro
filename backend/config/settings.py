import os
from pathlib import Path
from typing import Optional, Union

from pydantic import BaseSettings

from root import ROOT_DIR, root_path


class Settings(BaseSettings):
    project_name: str = "team03"
    project_version: str = "0.0.1"

    app_env: str

    postgres_user: Optional[str] = "postgres"
    postgres_password: Optional[str] = ""
    postgres_server: Optional[str] = "localhost"
    postgres_port: Optional[str] = 5432  # default postgres port is 5432
    postgres_db: Optional[str] = ""

    algorithm: str = "HS256"
    access_token_expire_minutes: float = 60 * 3
    secret_key: str

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_server}/{self.postgres_db}"

    class Config:
        env_file = Path(ROOT_DIR) / ".env"


class ProdSettings(Settings):
    app_env: str

    class Config:
        env_file = root_path(".env"), root_path(".env.prod")


class TestSettings(Settings):
    app_env: str = "testing"

    class Config:
        env_file = root_path(".env.test")


class LocalSettings(Settings):
    app_env: str = "development"

    class Config:
        env_file = root_path(".env.local")


APP_ENV = os.environ.get("APP_ENV", "development")

settings_dict = dict(
    development=LocalSettings, production=ProdSettings, test=TestSettings
)

DEFAULT_ENVIRONMENT = "development"
settings_cls = settings_dict.get(APP_ENV.lower(), DEFAULT_ENVIRONMENT)

settings: Union[LocalSettings, Settings, TestSettings] = settings_cls()

print(f"Running in app_env: {settings.app_env}")
