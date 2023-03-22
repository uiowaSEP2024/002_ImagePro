import psycopg2.errors
import pytest
import sqlalchemy

from app import models


def test_create_job(db, random_test_user):
    job = models.Job(
        client_job_id="abc123",
        client_job_kind="kidneyV1",
        customer_id=random_test_user.id,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    assert isinstance(job, models.Job)
    assert job.customer_id == random_test_user.id
    assert job.client_job_id == "abc123"
    assert job.client_job_kind == "kidneyV1"

    db.refresh(random_test_user)
    assert len(random_test_user.jobs) == 1


def test_create_job_missing_customer_id(db, random_test_user):
    job = models.Job(
        client_job_id="abc123",
        client_job_kind="kidneyV1",
    )

    db.add(job)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as exc:
        db.commit()

    # Check for null violation and that column is part of the error message in the error
    assert isinstance(exc.value.orig, psycopg2.errors.NotNullViolation)
    assert "customer_id" in str(exc.value.orig)


def test_create_job_missing_client_job_id(db, random_test_user):
    job = models.Job(
        customer_id=random_test_user.id,
        client_job_kind="kidneyV1",
    )

    db.add(job)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as exc:
        db.commit()

    # Check for null violation and that column is part of the error message in the error
    assert isinstance(exc.value.orig, psycopg2.errors.NotNullViolation)
    assert "client_job_id" in str(exc.value.orig)
