import argparse
import sys
import os
import psycopg2


def setup_app_config_settings(app_env):
    """
    Programmatically sets the APP_ENV variable for the application
    So that when settings are initialized, they are initialized with a known APP_ENV.
    """
    os.environ["APP_ENV"] = app_env
    import config.settings

    return config.settings


def create_conn(app_env):
    settings = setup_app_config_settings(app_env)

    conn = psycopg2.connect(
        user=settings.postgres_user,
        password=settings.postgres_password,
        host=settings.postgres_server,
        port=settings.postgres_port,
    )

    conn.autocommit = True
    return conn


def create_db(name, app_env):
    conn = None

    try:
        conn = create_conn(app_env)

        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        # Preparing query to create a database
        sql = f"""CREATE DATABASE {name}"""

        # Creating a database
        cursor.execute(sql)
        print(f"Database {name} created successfully...")

    except Exception as e:
        print(f"Database {name} creation failed.")
        print(e)

    finally:
        conn.close() if conn else None


def drop_db(name, app_env):
    conn = None
    try:
        conn = create_conn(app_env)

        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        # Preparing query to create a database
        sql = f"""DROP DATABASE IF EXISTS {name}"""

        # Creating a database
        cursor.execute(sql)
        print(f"Database {name} dropped successfully...")
    except Exception as e:
        print(e)
        print(f"Database {name} creation failed")

    finally:
        conn.close() if conn else None


"""
DB Creations
"""


def db_test_drop():
    drop_db("db_test", "test")


def db_dev_drop():
    drop_db("db_dev", "test")


def db_test_create():
    create_db("db_test", "test")


def db_dev_create():
    create_db("db_dev", "development")


def db_prod_create():
    create_db("postgres", "production")


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


# fmt: off
commands = {
    "db:test:reset": db_test_reset,
    "db:dev:reset": db_dev_reset,

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
