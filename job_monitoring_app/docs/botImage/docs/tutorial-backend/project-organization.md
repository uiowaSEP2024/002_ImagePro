---
sidebar_position: 0
---

# Project Organization

# Introduction

This page describes the organization of the project backend.

In summary, the backend project is a [FastAPI](https://fastapi.tiangolo.com/) application that is dockerized and deployed to [AWS](https://aws.amazon.com).


The backend project is organized as follows:

```txt
backend
├── Dockerfile
├── README.md
├── alembic
│   ├── env.py
│   └── versions
├── alembic.ini
├── app
│   ├── __init__.py
│   ├── dependencies.py
│   ├── internal
│   ├── main.py
│   ├── models
│   ├── routers
│   ├── schemas
│   └── services
├── config
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   └── settings.py
├── conftest.py
├── docker-compose.yml
├── requirements.txt
├── root.py
├── run-db.sh
├── run-dev.sh
├── run-test.sh
├── seed.py
├── tasks.py
└── tests
```

Now we will describe each of the files and directories in the project.

## `README.md`
This file contains the documentation for the backend application. It contains important information and useful commands for running and managing the application. You can find it [here](https://github.com/sep-23/team_03/tree/main/backend#readme)


## `Dockerfile`
This file contains the instructions for building the docker image for the backend application. It is put together using AWS documentation [here](https://docs.aws.amazon.com/lambda/latest/dg/images-create.html#images-create-from-base).

Some important caveats that were required when setting this up are the following:
* A version of Postgres that supports `scram-sha-256` authentication has to be enabled in the docker image. This authentication method is the most secure and [required by AWS RDS](https://aws.amazon.com/blogs/database/scram-authentication-in-rds-for-postgresql-13/). This is done by adding the following line to the Dockerfile:
```Dockerfile
# Install amazon-linux-extras
RUN yum install -y amazon-linux-extras

# Enable postgresql14 features to allow auto installing postgresql-devel-14 + libpq v10+
RUN PYTHON=python2 amazon-linux-extras enable postgresql14
```
The rest of the Dockerfile installs remaining dependencies as needed and copies over application code to the image.

The `CMD` instructions is set as follows, which calls the corresponding lambda handler in the application:
```Dockerfile
# ...

CMD [ "app/main.handler" ]
```

## `alembic`
This directory, along with `alembic.ini` were setup through Alembic's Installation [instructions](https://alembic.sqlalchemy.org/en/latest/front.html#installation).

The `alembic/env.py` file has been modified to reference the `config` directory for the database connection string. This allows us to perform migration tasks for different environments (e.g. development, test, production) by simply running the migration commands with the corresponding environment variables set.

See more details in the README's [Application Environments](https://github.com/sep-23/team_03/blob/main/backend/README.md#application-environments) and [Working with Database Migrations](https://github.com/sep-23/team_03/blob/main/backend/README.md#working-with-database-migrations) sections.

In summary, when performing some of the alembic scripts outlined in the alembic tutorial, you would run them as follows:
```bash
# Generating migrations
APP_ENV=production alembic revision --autogenerate -m "Add some feature"

# Upgrading migrations
APP_ENV=production alembic upgrade head
APP_ENV=development alembic upgrade head
APP_ENV=test alembic upgrade head

# Downgrading migrations
APP_ENV=production alembic downgrade -1
APP_ENV=development alembic downgrade -1
APP_ENV=test alembic downgrade -1
```

## `app`
This directory contains the application code. It has the following major subdirectories:

### `main.py`
This file is the entry-point into the application.

Important steps that are performed in this file include:
* Creating the FastAPI application
* Assembling all routers and including them in the application
* Configuring the application's environment on startup
* Creating and exposing the handler for AWS lambda. See the `CMD` instruction in the Dockerfile for how this handler is referenced.

```python
# ...

# Creating the FastAPI application
app = FastAPI()

# ...

# Configuring the app's environment
@app.on_event("startup")
async def startup_event():
    config.setup()

# ...

# Including all routers
app.include_router(users_router)
app.include_router(apikeys_router)

# ...


# Create handler for AWS lambda
handler = Mangum(app, lifespan="off")
```

### `dependencies.py`
Contains the [FastAPI Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/) for the application. Such dependencies include ones such as:
* `get_db` (for creating a database session)
* `get_current_user_from_token`: For authenticating users using a secure JWT token that is set in the user's browser cookies on authentication.
* `get_user_from_api_key`: For authenticating users using an API key that is provided by the users in the request header.

These Dependencies allows us to inject resources such as the current `user`, `db` session, as well as to intercept requests if the request lacks valid authentication.


### `internal`
This directory contains helper methods for the application. Currently some of the helper functions include `create_access_token` for creating a JWT token, `get_password_hash` for hashing passwords, and `verify_password` for verifying a password against a hashed password.



### `models`
This directory contains the SQLAlchemy models for the application. These models are used to define the database schema and are used by the application to interact with the database.

Some important models include: `User`, `Job`, `Event`, etc.

> **Note:**
> For models to be recognized by Alembic, they must be imported into `models/__init__.py`. The `Base` model from this file is in-turn imported inside of `alembic/env.py` to allow Alembic to recognize all models in the file that have extended base `Base`.

> Once all models are imported appropriately, migrations can be autogenerated whenever a model is changed. See [Auto Generating Migrations](https://github.com/sep-23/team_03/blob/main/backend/README.md#auto-generating-a-migration) for more details.

### `routers`
This directory contains the routers for the application. These routers are used to define the API endpoints for the application.

Important routes include:
* `users.py`: routes for creating, and retrieving users.
* `api_keys.py`: routes for creating and retrieving API keys for users.
* `auth.py`: routes for authenticating users and creating JWT tokens
* `jobs.py`: routes for creating and retrieving jobs
* `events.py`: routes for creating and retrieving events for jobs


### `schemas`
This directory contains the Pydantic schemas for the application. These schemas are used to define and validate the request and response models for the API endpoints.

In general the schema classes are defined in stages - with each stage being a class that inherits from the previous class. Shared properties are placed in the base class, and additional properties are added in subsequent classes.

The general convention is:
* `Base`: Contains the shared properties for the schema
* `Create`: Contains the properties for creating a new instance of the schema
* `Public`: Contains the properties that are publicly exposed for the schema. For example if we want to mask certain fields.

For example, the `User` schema is defined as follows:
```python
from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
```


Finally, these schemas can be used on a route as follows:
```python
from app import schemas

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return ...
```


### `services`
This directory contains CRUD operations for the application. Each function interacts with the database models to perform the corresponding CRUD operation.

These operations are intended to be usable by the routers to fulfill requests.

For example the router above fulfills the request as follows:
```python
from app import schemas, services

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return services.create_user(db=db, user=user)
```

The different dependencies that were injected by FastAPI such as the `db` session and `user` object are passed into the service method to be used to fulfill the request.


## `config`
This directory contains logic for configuring the backend. It contains the following files:

### `database.py`
This file exposes a `Database` class, which when initialized exposes a `SessionLocal` object that can be used instantiated to create a database session for interacting with the database.

This class is initialized with a `database_url` by the `Config` class in `config/config.py`.


### `settings.py`
This file exposes a `Settings` classes for each environment. Each of these `Settings` classes loads environment variables from a `.env` file in the root directory of the project.

There is a settings class for each environment: `LocalSettings`, `ProdSettings`, and `TestSettings`.

The appropriate settings class is initialized by the `Config` class in `config/config.py` based on the `APP_ENV` environment variable.


### `config.py`
This class exposes a `config` object which is an instance of the `Config` class. This `Config` class has helper function `setup(app_env)` which does the following:

* Determines the `app_env` from the supplied argument if provided, or from the `APP_ENV` environment variable.
* Sets up the appropriate `Settings` class from `config/settings.py` for the appropriate environment
*  Sets up the database using the `Database` class from `config/database.py`, and using the database url from the `Settings` instances' `database_url` property.


> 💡 The exposed `config` object is imported and used by other modules in the application to access the database session, and other environment variables.


## `run-db.sh`
This script is used to start a local Postgres database using Docker. Once started, the database is available for connections on the URL `postgresql://<user>:<password>@localhost/<database-name>`.

To use the script, run the following command:
```bash
bash run-db.sh
```

## `run-dev.sh`
This script is used to start the backend application in development mode.

To use the script, run the following command:
```bash
bash run-dev.sh
```

## `conftest.py`
This file is the entry point for `pytest`. It contains fixtures that are used by the tests in the `tests` directory.

We also use this file to configure the application in the `test` environment by making call to `config.setup("test")` at the top of the file.


Important fixtures include:
* `run_around_tests`: for automatically truncating all tables in the database before and after each test session (i.e each execution of `pytest`)
* `random_test_user_factory`: for creating random users for testing
* etc.


## `tasks.py`
This file contains helper scripts for managing the database. These scripts are wrappers around the `alembic` CLI and `psycopg2` library to handle common operations such as:
* Resetting (Dropping + Creating) a database
* Running migrations (Upgrading and Downgrading) a database
* Seeding a database with fake data, etc.

For finding out all available commands, run the following
```bash
python tasks.py -h
```

A common workflow for local development includes the following:
```bash
python tasks.py db:dev:reset
python tasks.py db:dev:upgrade
python tasks.py db:dev:seed
```

And then for testing:
```bash
python tasks.py db:test:upgrade
```

New commands can be added by adding new functions to the `tasks.py` file and decorating them with the `@task` decorator.

> Tip: Here as well, each task makes a call to `config.setup("<environment>")` to configure the application with the appropriate settings for the task.



## `seed.py`
This file exposes some helper functions for seeding the database. As mentioned above, seeds can be applied by running the `tasks.py` script.

```bash
python tasks.py db:dev:seed
```

The `seed.py` file is fairly new, but is organized as follows:

* **Entity Caches**: these are dictionaries that cache models inserted into the database that can be referred to when seeding other models. For example, the `users` dictionary is a dictionary that caches users that have been inserted into the database, with their emails as keys and the user object as values. This is useful for seeding other models that have a foreign key reference to the user model.
* **`<MODEL>_DATA`**: these contain the data to be seeded for each model. At this level, candidate keys are used to establish references between entities. For example for the `User` model, we can use `email` as a candidate key to reference users in `MODEL_DATA` definitions.
* **`seed_<model>`**: these are functions that seed the database with data for each model. They are called by the `seed_db` function which is in turn called by the `tasks.py` script.
* **`seed_db`**: this function is called by the `tasks.py` script to seed the database. It calls the `seed_<model>` functions to seed each model in the database. It first establishes a database connection using `config.database.SessionLocal`, relying on the environment that would have already been prepared by the `tasks.py` script.


## `root.py`
This file is meant to be kept in the root directory of the `backend`. It exposes a `ROOT_DIR` variable that stores the absolute path to the root directory of the project, as well as a  `root_path(path)` function that prepends the given `path` with the `ROOT_DIR`.

It is used for example by the `Settings` classes in `config/settings.py` to load the `.env` files from the root directory of the project.
