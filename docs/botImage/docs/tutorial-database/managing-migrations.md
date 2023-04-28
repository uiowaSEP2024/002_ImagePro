---
sidebar_position: 3
---

# Managing Migrations

For all the following scripts, the value of `APP_ENV` is set to one of the available environments: `development`, `production` or `test`.

### Starting Database

Ensure that the [Docker](https://docs.docker.com/get-docker/) Desktop Application has been installed and is running. We will use Docker to to start a local Postgres database using the following script:

```bash
bash run-db.sh
```

Once started, the database is available for connections on the `URL postgresql://<user>:<password>@localhost/<database-name>`

### Running Migrations

The following command applies all migrations to the database in the targeted environment:

```bash
APP_ENV=<environment> alembic upgrade head
```

In the above, `head` is a 'revision', and can be swapped for a specific revision id or be relative, such a `+1` for upgrading to the next revision.

### Reset Migrations

The following command reverts migrations (drops + creates the database):

```bash
python tasks.py db:<APP_ENV>:reset
```

### Upgrading Migrations

The following command upgrades migrations:

```bash
python tasks.py db:<APP_ENV>:upgrade
```

### Downgrading Migrations

The following command downgrades migrations:

```bash
python tasks.py db:<APP_ENV>:downgrade
```
