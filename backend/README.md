# backend
This is the backend project for Team03's SEP project.


# Getting Started
1. Make sure you have Python installed (preferably v3.10), which you can download from [here](https://www.python.org/downloads/)
2. Before starting the application, make sure to create a virtual environment for the project:
   ```bash
   python -m venv .venv 
   ```
3. Next, activate the virtual environment. **NB: You will have to do this step every time you start/open a fresh terminal**
   ```bash
   source venv/bin/activate
   ```
   > If you are working in PyCharm, steps 2 and 3 should be performed automatically for you.

4. Once the virtual environment is started, make sure to install all requirements required for the project:
   ```bash
   pip install -r requirements.txt
   ```
   
5. Create a file called .env.local, and then copy and paste the contents from .env.example file
   into it, replacing with your own values as appropriate.

6. Finally, to start the application, run the following script:
   ```bash
   bash run-dev.sh
   ```

# Application Environments
The environment that the application runs in determines the application's configuration,
including secrets, the database's URL and more.

When starting the application, or running other application commands
you will need to provide an appropriate `APP_ENV`, so the application
loads environment variables from corresponding environment variables files.

This table outlines the different application environments, and where environment variables for that environment
are loaded from:

| Environment   | Environment Variables File |
|:--------------|:---------------------------|
| `production`  | .env, .env.prod            |
| `development` | .env.local                 |
| `test`        | .env.test                  |

> NB: If you don't provide an environment variable, the app will fail to start.

> NB: For security reasons, a `SECRET_KEY` is also required when `APP_ENV` is production.
> For the simple scenario of generating something such as a migration, you may set this to
> any string locally inside your .env or .env.prod. The real SECRET_KEY would be configured securely
> from an AWS console.

# Working with Database Migrations
Here are some scripts for working with migrations. For all the following commands,
using we are setting `APP_ENV` to some environment (namely: `development`, `production`, or `test`).

### Auto-generating a Migration
To autogenerate a migration, first add your new model to `app/models`, or edit an existing model.

> NB: If you are adding a new model, you will have to explicitly import it inside of `app/models/__init__.py`,
> so that it is included in the runtime, when alembic is performing the auto-generation.

Finally, run the following command to auto-generate the migrations:
```bash
APP_ENV=<environment> alembic revision --autogenerate -m "migration_name"
```
> NB: In general we want to auto-generate migrations against the state of the
> production database, as the source of truth for the state of the application's database.

### Running Migrations
Use the following command to apply all migrations to the database in the targeted environment
```bash
APP_ENV=<environment> alembic upgrade head
```
In the above, `head` is a 'revision', and can be swapped for a specific revision id
or be relative, such a `+1` for upgrading to the next revision.

### Reset Migrations
Use the following script to revert migrations
```bash
APP_ENV=<environment> alembic downgrade base
```

In the above, `base` is a 'revision' is the very first revision. 
It can be replaced with a specific revision id
or be relative, such a `-1` for downgrading to the last revision.

> NB: In general, we do not want to run this command targeted against the production
> environment (that is, the production database).

# Testing
To execute tests, run:

(With test coverage)
```bash
bash run-test.sh
```

OR

```bash
pytest
```

> NB: The file, `conftest.py` is `pytest`'s entrypoint to running tests
> and has logic to automatically configure the application to run in the `test` environment.

# Deployment 
For deployment instructions to AWS, see `cdk-infra` project!

However, for simulating a deployment locally you can follow the follow these
steps to spin up the application in a Docker container.

There are two ways to start the application: 
1. Manually Using Docker 
2. Using Docker Compose (which automatically also spins up a Postgres Database in another Docker container)

### Manually Using Docker

1. Build the docker image
    ```bash
   docker build --build-arg APP_ENV=development -t team8-backend .    
   ```
2. Run the docker image
   ```bash
   docker run --env-file .env.local -e APP_ENV=development -p 9000:8080 team8-backend
   ```
3. Now you may interact with the running container by making a cURL request with
   an API Gateway event payload such as in the `event.json` file.

   Modify the `resources` and `path` keys to target different endpoints of the application.
   
   Once you have edited the `event.json` to suite the request you would like to make, use the following command to issue
   the request to the running container:
   
   ```bash
   curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d @event.json
   ```
 
> Note: The above instructions have been adapted from AWS documentation [here](https://docs.aws.amazon.com/lambda/latest/dg/images-create.html). See "Creating images from AWS base images" section.  

> Note: In this approach, you are responsible for making sure that you have a database up and running
> for the application to use.

### Using Docker Compose
1. Build the docker images for the application and database using
   ```bash
   docker compose build
   ```
2. Start containers for both the application and database using
   ```bash
   docker compose up
   ```
3. Finally, you can make requests similar to the above in Step 3 with `curl` or using an HTTP client such as Postman or Insomnia.

> NB: This approach is currently only configured for the 'development' environment. The database contents are
> persisted in a `pg_data` file within the same directory, so that data placed in the development environment
> during local development remains after the container is destroyed.
> If you want to start with a fresh database, you can delete `pg_data` directory.