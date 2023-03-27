import argparse
import sys
import os
import psycopg2


def setup_app_settings(app_env):
    """
    Programmatically sets the APP_ENV variable for the application
    So that when settings are initialized, they are initialized with a known APP_ENV.
    """
    os.environ["APP_ENV"] = app_env
    import config.settings

    return config.settings


def create_conn(settings):
    conn = psycopg2.connect(
        user=settings.postgres_user,
        password=settings.postgres_password,
        host=settings.postgres_server,
        port=settings.postgres_port,
    )

    conn.autocommit = True
    return conn


def create_db(settings):
    conn = None

    try:
        conn = create_conn(settings)

        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        # Preparing query to create a database
        sql = f"""CREATE DATABASE {settings.postgres_db}"""

        # Creating a database
        cursor.execute(sql)
        print(f"Database {settings.postgres_db} created successfully...")

    except Exception as e:
        print(f"Database {settings.postgres_db} creation failed.")
        print(e)

    finally:
        conn.close() if conn else None


def drop_db(settings):
    conn = None
    try:
        conn = create_conn(settings)

        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        # Preparing query to create a database
        sql = f"""DROP DATABASE IF EXISTS {settings.postgres_db}"""

        # Creating a database
        cursor.execute(sql)
        print(f"Database {settings.postgres_db} dropped successfully...")
    except Exception as e:
        print(e)
        print(f"Database {settings.postgres_db} creation failed")

    finally:
        conn.close() if conn else None


"""
DB Creations
"""


def db_test_drop():
    settings = setup_app_settings("test")
    drop_db(settings)


def db_dev_drop():
    settings = setup_app_settings("development")
    drop_db(settings)


def db_test_create():
    settings = setup_app_settings("test")
    create_db(settings)


def db_dev_create():
    settings = setup_app_settings("development")
    create_db(settings)


def db_prod_create():
    settings = setup_app_settings("production")
    create_db(settings)


"""
Migrations
"""


def db_test_migrate(revision="head"):
    db_test_create()
    os.system(f"alembic upgrade {revision}")


def db_migrate(app_env, direction, revision):
    os.environ["APP_ENV"] = app_env
    os.system(f"alembic {direction} {revision}")


def db_dev_migrate_up(revision="head"):
    db_migrate("development", "upgrade", revision)


def db_dev_migrate_down(revision="base"):
    db_migrate("development", "downgrade", revision)


def db_test_migrate_down(revision="base"):
    db_migrate("test", "downgrade", revision)


def db_test_migrate_up(revision="head"):
    db_migrate("test", "upgrade", revision)


def db_prod_migrate_up(revision="head"):
    db_migrate("production", "upgrade", revision)


def db_test_reset():
    db_test_drop()
    db_test_create()


def db_dev_reset():
    db_dev_drop()
    db_dev_create()


users_data = [
    # Customers
    dict(email="johndoe@gmail.com", password="abc"),
    dict(email="janeblack@gmail.com", password="abc"),
    # Providers
    dict(email="noodlesco@gmail.com", password="abc"),
    dict(email="botimage@gmail.com", password="abc"),
]

jobs_data = [
    # Job 1
    dict(
        customer_email="johndoe@gmail.com",
        provider_email="botimage@gmail.com",
        provider_job_id="botimage-123",
        provider_job_name="KidneyV1",
    ),
    # Job 2
    dict(
        customer_email="janeblack@gmail.com",
        provider_email="botimage@gmail.com",
        provider_job_id="noodlesco-123",
        provider_job_name="LungsV3",
    ),
]


events_data = [
    #  Job botimage-123, Event 2
    dict(
        provider_job_id="botimage-123",
        kind="step",
        name="Scanning Left Kidney",
    ),
    #  Job botimage-123, Event 3
    dict(
        provider_job_id="botimage-123",
        kind="step",
        name="Scanning Right Kidney",
    ),
    #  Job botimage-123, Event 4
    dict(
        provider_job_id="botimage-123",
        kind="step",
        name="Analyze Kidney Results",
    ),
    #  Job noodlesco-123, Event 2
    dict(
        provider_job_id="noodlesco-123",
        kind="step",
        name="Scanning Left Lung",
    ),
    #  Job noodlesco-123, Event 3
    dict(
        provider_job_id="noodlesco-123",
        kind="step",
        name="Scanning Right Lung",
    ),
    #  Job noodlesco-123, Event 4
    dict(
        provider_job_id="noodlesco-123",
        kind="step",
        name="Analyze Lung Results",
    ),
]


def db_dev_seed():
    db_dev_drop()
    db_dev_create()
    db_dev_migrate_up()

    from app import models
    from config.database import SessionLocal
    from app.internal import get_password_hash

    db = SessionLocal()

    users = {}
    jobs = {}
    events = {}

    for data in users_data:
        user = models.User(
            email=data["email"], hashed_password=get_password_hash(data["password"])
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        users[user.email] = user

    for data in jobs_data:
        customer_id = users[data["customer_email"]].id
        provider_id = users[data["provider_email"]].id

        job = models.Job(
            customer_id=customer_id,
            provider_id=provider_id,
            provider_job_name=data["provider_job_name"],
            provider_job_id=data["provider_job_id"],
        )

        db.add(job)
        db.commit()
        db.refresh(job)

        jobs[job.provider_job_id] = job

    for data in events_data:
        job = jobs[data["provider_job_id"]]

        event = models.Event(
            job_id=job.id,
            kind=data["kind"],
            name=data["name"],
        )

        db.add(event)
        db.commit()
        db.refresh(event)

        events[event.id] = event


# fmt: off
commands = {
    "db:test:reset": db_test_reset,
    "db:dev:reset": db_dev_reset,

    "db:dev:seed": db_dev_seed,

    "db:dev:upgrade": db_dev_migrate_up,
    "db:test:upgrade": db_test_migrate_up,
    "db:prod:upgrade": db_prod_migrate_up,

    "db:dev:downgrade": db_dev_migrate_down,
    "db:test:downgrade": db_test_migrate_down,
}

parser = argparse.ArgumentParser(prog="botimage")

parser.add_argument('command', choices=commands.keys())

if __name__ == "__main__":
    args = sys.argv[1:]
    print(f'Received args: {args}')

    parsed_args, rest_args = parser.parse_known_args(args)

    as_dict = vars(parsed_args)

    print(f'Args as dict: {as_dict}')

    if not parsed_args.command:
        print(parser.error(f'Unrecognized command: {" ".join(args)}'))
    else:
        command = parsed_args.command
        command_args = rest_args

        method = commands.get(command, None)
        if method:
            method(*command_args)
