import psycopg2.errors
import pytest
import sqlalchemy

from ...app import models


def test_create_event(db, random_test_user, random_provider_user):
    job = models.Job(
        provider_job_id="abc123",
        provider_job_name="kidneyV1",
        customer_id=random_test_user.id,
        provider_id=random_provider_user.id,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    # Create events for the job

    event = models.Event(
        job_id=job.id,
        name="Scanning Kidney",
        kind="step",
        event_metadata={"unofficial": "Yes"},
    )

    db.add(event)
    db.commit()
    db.refresh(event)
    db.refresh(job)

    assert event.job_id == job.id
    assert event.kind == "step"
    assert event.name == "Scanning Kidney"
    assert event.event_metadata == {"unofficial": "Yes"}
    assert event.created_at is not None

    assert len(job.events) == 1
    assert event.job.id == job.id


def test_create_event_missing_job_id(db):
    event = models.Event(name="Scanning Kidney", kind="step")

    db.add(event)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as exc:
        db.commit()

    assert isinstance(exc.value.orig, psycopg2.errors.NotNullViolation)
    assert "job_id" in str(exc.value.orig)


def test_create_job_missing_kind(db, random_test_user, random_provider_user):
    job = models.Job(
        provider_job_name="kidneyV1",
        customer_id=random_test_user.id,
        provider_id=random_provider_user.id,
    )

    db.add(job)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as exc:
        db.commit()

    # Check for null violation and that column is part of the error message in the error
    assert isinstance(exc.value.orig, psycopg2.errors.NotNullViolation)
    assert "provider_job_id" in str(exc.value.orig)


def test_create_job_missing_provider_job_name(
    db, random_test_user, random_provider_user
):
    job = models.Job(
        provider_job_id="abc123",
        provider_job_name="kidneyV1",
        customer_id=random_test_user.id,
        provider_id=random_provider_user.id,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    # Create events for the job

    event = models.Event(job_id=job.id, name="Scanning Kidney")

    db.add(event)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as exc:
        db.commit()

    assert isinstance(exc.value.orig, psycopg2.errors.NotNullViolation)
    assert "kind" in str(exc.value.orig)


def test_create_event_for_step(
    db, random_test_user, random_provider_user, random_job_configuration_factory
):
    job_configuration = random_job_configuration_factory.get(num_steps=1)

    job = models.Job(
        provider_job_id="abc123",
        provider_job_name="kidneyV1",
        customer_id=random_test_user.id,
        provider_id=random_provider_user.id,
        job_configuration_id=job_configuration.id,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    # Create events for the job

    event = models.Event(
        job_id=job.id,
        name="Scanning Kidney",
        kind="step",
        step_configuration_id=job_configuration.step_configurations[0].id,
    )

    db.add(event)
    db.commit()
    db.refresh(event)
    db.refresh(job)

    assert event.step_configuration_id == job_configuration.step_configurations[0].id
