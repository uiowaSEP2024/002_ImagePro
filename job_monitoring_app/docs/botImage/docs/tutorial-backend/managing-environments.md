---
sidebar_position: 1
---

# Managing Environments

# Introduction
Environment variables can be used to modify how the application runs depending on whether it is running locally, or in a test environment or in production.

Environment variables help us to store sensitive information like API keys, database credentials, etc.

## Settings Class
The approach taken to manage environment variables is through a `Settings` class that inherits from [Pydantic's BaseSettings](https://docs.pydantic.dev/usage/settings/).


The `Settings` class automatically loads environment variables from within the current environment, or from the specified `.env[.<environment>]` file if one exists.

For example we have the following basic `Settings` class:

```python
from typing import Optional
from pydantic import BaseSettings

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
```

##  ProdSettings, LocalSettings and TestSettings Classes
For each environment, we create a class that inherits from the `Settings` class and overrides some default values, as well as the `Config` class to specify an appropriate `.env[.<environment>]` file to load from.

For example for production settings, we have:

```python
from root import root_path

class ProdSettings(Settings):
    app_env: str = "production"
    secret_key: str

    class Config:
        env_file = root_path(".env"), root_path(".env.prod")
```
> In production, we want to absolutely have a `secret_key` specified, so we make it a required field. We also specify that the `.env.prod` file should be loaded in addition to the default `.env` file if available, with `.env.prod` taking precedence.

## Instantiating Settings Class
We need to instantiate the settings class to be able to use the environment variables. For instantiating the appropriate settings class, we also need to know what environment we are in.

The application environment is determined by the `APP_ENV` environment variable.

The file `config.py` has a `Config` class with a `setup` function that instantiates the appropriate settings class based on the `APP_ENV` environment variable.

See the specific implementation in [`config.py`](https://github.com/sep-23/team_03/blob/main/backend/config/config.py) for more.

To use the settings class, we simply import `config` variable from `config.py`, make a call to `config.setup()` and then access the settings class through `config.settings`.

```python
from config import config

config.setup("development")
# or config.setup("production")
# or config.setup("test")

print(config.settings.dict())
```

Result
```txt
{'project_name': 'team03', 'project_version': '0.0.1', 'app_env': 'development', 'postgres_user': 'postgres', 'postgres_password': 'mypostgresspassword', 'postgres_server': 'localhost', 'postgres_port': '5432', 'postgres_db': 'db_dev', 'algorithm': 'HS256', 'access_token_expire_minutes': 180.0, 'secret_key': 'H3llo'}
```


## Controlling Environment Variables
There are many ways to control environment variables.

### Using Command Line
You can set environment variables through the command line. For example, to set the `APP_ENV` environment variable to `development`, you can do:

```bash
export APP_ENV=development
uvicorn app.main:app --reload
```
After this, subsequent calls to `config.setup()` (NB: without an argument for the `app_env`) everywhere in the application will instantiate the `LocalSettings` class.

On the other hand, you can also inline the environment variable when starting the application locally. For example, `run-dev.sh` does this:

```bash
APP_ENV='development' uvicorn app.main:app --reload
```


### Environment Files
When running locally, you can easily do so through the `.env[.<environment>]` files.

See the [README](https://github.com/sep-23/team_03/tree/main/backend#application-environments) for the correct `.env[.<environment>]` files for each environment. Here is a copy below:

| Environment   | Environment Variables File |
|:--------------|:---------------------------|
| `production`  | .env, .env.prod            |
| `development` | .env.local                 |
| `test`        | .env.test                  |

### Deployment Environment Variables
Once deployed to AWS Lambda, environment variables can be set through the AWS Lambda console.

Here are some images to help you out:

![AWS Lambda Console](/img/lambda-configuration.png)
![AWS Lambda Console Configuration Environment Variables](/img/lambda-configuration-environment-variables.png)
