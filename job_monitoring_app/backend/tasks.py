import argparse
import os
import sys

import psycopg2
from app.config import config
from seed import seed_db


def task(func):
    def logged(*args, **kwargs):
        print(f"---- {func.__name__} ---")
        result = func(*args, **kwargs)
        return result

    return logged


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
    config.setup("test")
    drop_db(config.settings)


def db_dev_drop():
    config.setup("development")
    drop_db(config.settings)


@task
def db_test_create():
    config.setup("test")
    create_db(config.settings)


@task
def db_dev_create():
    config.setup("development")
    create_db(config.settings)


@task
def db_prod_create():
    config.setup("production")
    create_db(config.settings)


"""
Migrations
"""


def run_migration(direction, revision):
    os.system(f"APP_ENV={config.settings.app_env} alembic {direction} {revision}")


@task
def db_dev_upgrade(revision="head"):
    config.setup("development")
    run_migration("upgrade", revision)


@task
def db_dev_downgrade(revision="base"):
    config.setup("development")
    run_migration("downgrade", revision)


@task
def db_test_downgrade(revision="base"):
    config.setup("test")
    run_migration("downgrade", revision)


@task
def db_test_upgrade(revision="head"):
    config.setup("test")
    run_migration("upgrade", revision)


@task
def db_prod_upgrade(revision="head"):
    config.setup("production")
    run_migration("upgrade", revision)


@task
def db_test_reset():
    db_test_drop()
    db_test_create()


@task
def db_dev_reset():
    db_dev_drop()
    db_dev_create()


@task
def db_dev_seed():
    config.setup("development")
    seed_db()


@task
def db_dev_seed_auto():
    config.setup("development")
    db_dev_reset()
    db_dev_upgrade()
    db_dev_seed()


# fmt: off
commands = {
    "db:test:reset": db_test_reset,
    "db:dev:reset": db_dev_reset,

    "db:dev:seed": db_dev_seed,
    "db:dev:seed_auto": db_dev_seed_auto,


    "db:dev:upgrade": db_dev_upgrade,
    "db:test:upgrade": db_test_upgrade,
    "db:prod:upgrade": db_prod_upgrade,

    "db:dev:downgrade": db_dev_downgrade,
    "db:test:downgrade": db_test_downgrade,
}

parser = argparse.ArgumentParser(prog="botimage")

parser.add_argument('command', choices=commands.keys())

if __name__ == "__main__":
    file_name = __file__.split("/")[-1]
    print(f'--- {file_name} ---')

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
