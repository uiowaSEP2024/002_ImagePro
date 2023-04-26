import os
from typing import Literal
from .database import Database
from .settings import settings_dict


class Config:
    def __init__(self):
        self._settings = None
        self._db = None

    def setup(self, app_env: Literal["production", "development", "test"] = None):
        self.__setup_settings(app_env)
        self.__setup_database(self.settings.database_url)

    def __setup_settings(
        self, app_env: Literal["production", "development", "test"] = None
    ):
        app_env = app_env if app_env else os.environ.get("APP_ENV")

        # Load settings corresponding to the APP_ENV
        settings_cls = settings_dict.get(app_env.lower())

        if not settings_cls:
            valid_keys = " | ".join(settings_dict.keys())
            raise EnvironmentError(
                f"Invalid value for APP_ENV environment variable. Expected any of: {valid_keys} \n"
                f"If running command from a shell, run the command as follows:\n"
                f"\tAPP_ENV=<environment> <command>\n"
                f"Alternatively, if running via AWS Lambda, set the APP_ENV at\n"
                f"\tConfiguration->Environment variables->Edit"
            )

        self._settings = settings_cls()

        print(f"Running in app_env: {self.settings.app_env}")
        print(f"Running with postgres_server: {self.settings.postgres_server}")
        print(f"Running with postgres_db: {self.settings.postgres_db}")

        return self.settings

    def __setup_database(self, database_url: str):
        if self.settings:
            self._db = Database(database_url)
        return self._db

    @property
    def settings(self):
        if not self._settings:
            raise Exception(
                "config - Settings not set up. Call config.setup() to set up settings"
            )
        return self._settings

    @property
    def db(self) -> Database:
        if not self._db:
            raise Exception(
                "config - Database not set up. Call config.setup() to set up db"
            )
        return self._db


# Singleton config instance, exposing the application settings, and database configuration
config = Config()
