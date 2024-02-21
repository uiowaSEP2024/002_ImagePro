import psycopg2.errors
import pytest
import sqlalchemy

from ...app import models


def test_create_job_configurtaion(db, random_provider_user):
    job_configuration = models.JobConfiguration(
        tag="prostate_v1_job",
        name="Prostate Job",
        provider_id=random_provider_user.id,
        version="1.1",
    )

    db.add(job_configuration)
    db.commit()
    db.refresh(job_configuration)

    assert isinstance(job_configuration, models.JobConfiguration)
    assert job_configuration.provider_id == random_provider_user.id
    assert job_configuration.tag == "prostate_v1_job"
    assert job_configuration.name == "Prostate Job"

    db.refresh(random_provider_user)
    assert len(random_provider_user.job_configurations) == 1
    assert random_provider_user.job_configurations[0].tag == "prostate_v1_job"
    assert (
        random_provider_user.job_configurations[0].provider_id
        == random_provider_user.id
    )


def test_duplicate_job_configuration_tag_and_version(db, random_provider_user):
    job_configuration1 = models.JobConfiguration(
        tag="prostate_v1_job",
        name="Prostate Job",
        provider_id=random_provider_user.id,
        version="1.2.8",
    )
    db.add(job_configuration1)
    db.commit()

    job_configuration1 = models.JobConfiguration(
        tag="prostate_v1_job",
        name="Prostate Job",
        provider_id=random_provider_user.id,
        version="1.2.8",
    )
    db.add(job_configuration1)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as exc:
        db.commit()

    assert isinstance(exc.value.orig, psycopg2.errors.UniqueViolation)
    assert (
        'violates unique constraint "job_configurations_provider_id_tag_version_key"'
        in str(exc.value.orig)
    )


def test_missing_tag(db, random_provider_user):
    job_configuration = models.JobConfiguration(
        name="Prostate Job",
        provider_id=random_provider_user.id,
        version="1.2.1",
    )
    db.add(job_configuration)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as exc:
        db.commit()

    assert isinstance(exc.value.orig, psycopg2.errors.NotNullViolation)
    assert "tag" in str(exc.value.orig)


#
def test_create_job_missing_job_configuration_name(db, random_provider_user):
    job_configuration1 = models.JobConfiguration(
        tag="prostate_v1_job", provider_id=random_provider_user.id, version="1.2.1"
    )
    db.add(job_configuration1)
    with pytest.raises(sqlalchemy.exc.IntegrityError) as exc:
        db.commit()

    # Check for null violation and that column is part of the error message in the error
    assert isinstance(exc.value.orig, psycopg2.errors.NotNullViolation)
    assert "name" in str(exc.value.orig)


def test_create_job_missing_provider_id(db):
    job_configuration1 = models.JobConfiguration(
        tag="prostate_v1_job",
        name="Prostate Job",
        version="1.2.1",
    )
    db.add(job_configuration1)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as exc:
        db.commit()

        # Check for null violation and that column is part of the error message in the error
    assert isinstance(exc.value.orig, psycopg2.errors.NotNullViolation)
    assert "provider_id" in str(exc.value.orig)


#
def test_create_job_missing_version(db, random_provider_user):
    job_configuration = models.JobConfiguration(
        tag="prostate_v1_job",
        name="Prostate Job",
        provider_id=random_provider_user.id,
    )
    db.add(job_configuration)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as exc:
        db.commit()

    assert isinstance(exc.value.orig, psycopg2.errors.NotNullViolation)
    assert "version" in str(exc.value.orig)
