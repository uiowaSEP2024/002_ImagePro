import psycopg2.errors
import pytest
import sqlalchemy

from app import models


def test_create_job(db, random_test_user, random_provider_user):
    job_configuration = models.JobConfiguration(
        tag="prostate_v1_job",
        name="Prostate Job",
        provider_id=random_provider_user.id,
        version="1.1",
    )

    db.add(job_configuration)
    db.commit()

    job = models.Job(
        provider_job_id="abc123",
        provider_job_name="kidneyV1",
        customer_id=random_test_user.id,
        provider_id=random_provider_user.id,
        job_configuration=job_configuration,
    )

    db.add(job)
    db.commit()

    db.refresh(job)

    assert isinstance(job, models.Job)
    assert job.customer_id == random_test_user.id
    assert job.provider_job_id == "abc123"
    assert job.provider_job_name == "kidneyV1"
    assert job.job_configuration == job_configuration
    assert job.created_at is not None

    db.refresh(random_test_user)
    # Check that the customer user now has the correct jobs associated with them
    assert len(random_test_user.jobs) == 1
    assert random_test_user.jobs[0].provider_job_id == "abc123"
    assert random_test_user.jobs[0].customer_id == random_test_user.id

    db.refresh(random_provider_user)
    # Check that the provider user now has the correct jobs associated with them
    assert len(random_provider_user.provider_jobs) == 1
    assert random_provider_user.provider_jobs[0].provider_job_id == "abc123"
    assert random_provider_user.provider_jobs[0].provider_id == random_provider_user.id
    assert random_provider_user.provider_jobs[0].job_configuration == job_configuration

    assert random_provider_user.provider_job_configurations[0] == job_configuration


def test_create_job_duplicate_provider_job_ids(
    db, random_test_user, random_provider_user
):
    job_configuration = models.JobConfiguration(
        tag="prostate_v1_job",
        name="Prostate Job",
        provider_id=random_provider_user.id,
        version="1.1",
    )

    db.add(job_configuration)
    db.commit()

    duplicate_job_id = "abc123"

    job1 = models.Job(
        provider_job_id=duplicate_job_id,
        provider_job_name="kidneyV1",
        customer_id=random_test_user.id,
        provider_id=random_provider_user.id,
        job_configuration=job_configuration,
    )

    db.add(job1)
    db.commit()

    job2 = models.Job(
        provider_job_id=duplicate_job_id,
        provider_job_name="kidneyV1",
        customer_id=random_test_user.id,
        provider_id=random_provider_user.id,
        job_configuration=job_configuration,
    )

    db.add(job2)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as exc:
        db.commit()

    # Check for null violation and that column is part of the error message in the error
    assert isinstance(exc.value.orig, psycopg2.errors.UniqueViolation)
    assert 'violates unique constraint "jobs_provider_id_provider_job_id_key"' in str(
        exc.value.orig
    )


def test_create_job_missing_customer_id(db, random_test_user, random_provider_user):
    job_configuration = models.JobConfiguration(
        tag="prostate_v1_job",
        name="Prostate Job",
        provider_id=random_provider_user.id,
        version="1.1",
    )

    db.add(job_configuration)
    db.commit()

    job = models.Job(
        provider_job_id="abc123",
        provider_job_name="kidneyV1",
        provider_id=random_provider_user.id,
        job_configuration=job_configuration,
    )

    db.add(job)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as exc:
        db.commit()

    # Check for null violation and that column is part of the error message in the error
    assert isinstance(exc.value.orig, psycopg2.errors.NotNullViolation)
    assert "customer_id" in str(exc.value.orig)


def test_create_job_missing_provider_job_id(db, random_test_user, random_provider_user):
    job_configuration = models.JobConfiguration(
        tag="prostate_v1_job",
        name="Prostate Job",
        provider_id=random_provider_user.id,
        version="1.1",
    )

    db.add(job_configuration)
    db.commit()
    job = models.Job(
        provider_job_name="kidneyV1",
        customer_id=random_test_user.id,
        provider_id=random_provider_user.id,
        job_configuration=job_configuration,
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
    job_configuration = models.JobConfiguration(
        tag="prostate_v1_job",
        name="Prostate Job",
        provider_id=random_provider_user.id,
        version="1.1",
    )

    db.add(job_configuration)

    job = models.Job(
        provider_job_id="abc123",
        customer_id=random_test_user.id,
        provider_id=random_provider_user.id,
        job_configuration=job_configuration,
    )

    db.add(job)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as exc:
        db.commit()

    # Check for null violation and that column is part of the error message in the error
    assert isinstance(exc.value.orig, psycopg2.errors.NotNullViolation)
    assert "provider_job_name" in str(exc.value.orig)


def test_create_job_missing_job_configuration(
    db, random_provider_user, random_test_user
):
    job = models.Job(
        provider_job_id="abc123",
        provider_job_name="kidneyV1",
        customer_id=random_test_user.id,
        provider_id=random_provider_user.id,
    )

    db.add(job)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as exc:
        db.commit()

    # Check for null violation and that column is part of the error message in the error
    assert isinstance(exc.value.orig, psycopg2.errors.NotNullViolation)
    assert "job_configuration" in str(exc.value.orig)
