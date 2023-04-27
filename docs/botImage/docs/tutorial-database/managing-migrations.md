---
sidebar_position: 3
---

# Managing Migrations

For all the following scripts, the value of `APP_ENV` is set to one of the available environments: `development`, `production` or `test`.

### Running Migrations

The following command applies all migrations to the database in the targeted environment:

```bash
APP_ENV=<environment> alembic upgrade head
```

In the above, `head` is a 'revision', and can be swapped for a specific revision id or be relative, such a `+1` for upgrading to the next revision.

### Reset Migrations

The following command reverts migrations:

```bash
python tasks.py db:<APP_ENV>:reset
```

In the above, `base` is a 'revision' is the very first revision. It can be replaced with a specific revision id or be relative, such a `-1` for downgrading to the last revision.
