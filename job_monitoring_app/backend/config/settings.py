from typing import Optional
from pydantic import BaseSettings
from job_monitoring_app.backend.root import root_path


class Settings(BaseSettings):
    project_name: str = "team03"
    project_version: str = "0.0.1"

    app_env: str = "development"

    postgres_user: Optional[str] = "postgres"
    postgres_password: Optional[str] = ""
    postgres_server: Optional[str] = "localhost"
    postgres_port: Optional[str] = 5432  # default postgres port is 5432
    postgres_db: Optional[str] = ""

    algorithm: str = "HS256"
    access_token_expire_minutes: float = 60 * 3
    secret_key: str = "H3llo"

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_server}/{self.postgres_db}"

    class Config:
        env_file = root_path(".env")


class ProdSettings(Settings):
    app_env: str = "production"
    secret_key: str

    class Config:
        env_file = root_path(".env"), root_path(".env.prod")


class TestSettings(Settings):
    app_env: str = "test"

    class Config:
        env_file = root_path(".env.test")


class LocalSettings(Settings):
    app_env: str = "development"

    class Config:
        env_file = root_path(".env.local")


settings_dict = dict(
    development=LocalSettings, production=ProdSettings, test=TestSettings
)
