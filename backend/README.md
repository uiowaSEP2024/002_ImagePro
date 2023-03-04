# backend
This is the backend project for Team03's SEP project.


# Get Started

Before starting the application, make sure to start a Virtual Environment for your project by using the command:

```bash
source venv/bin/activate
```

Once the Venv is fired up, make sure to install all requirements required for the project:

```bash
pip install -r requirements.txt
```

To start the application, run:

```bash
bash run-dev.sh
```

OR

```bash
uvicorn app.main:app --reload
```


# Running Migrations
Here are some scripts for working with migrations:

**Autogenerate a new migration**
```bash
alembic revision --autogenerate -m "<migration_name>"
```

**Apply all migrations**
```bash
alembic upgrade head
```

**Reset all migrations**

```bash
alembic downgrade base
```

**Reset last migration**
```bash
alembic downgrade -1
```

# Run Tests
To execute tests, run:

(With test coverage)
```bash
bash run-test.sh
```

OR

```bash
pytest
```

