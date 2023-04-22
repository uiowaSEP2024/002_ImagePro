import psycopg2.errors
import pytest
import sqlalchemy

from app import models


def test_create_step_configuration(db, random_provider_user):
    job_configuration = models.JobConfiguration(
        tag="prostate_v1_job",
        provider_job_configuration_name="Prostate Job",
        provider_id=random_provider_user.id,
    )

    db.add(job_configuration)
    db.commit()
    db.refresh(job_configuration)

    step_configuration = models.StepConfiguration(
        job_tag="prostate_v1_job",
        tag="kidney_scan",
        provider_step_configuration_name="Kidney Scan",
        points=20,
        job_configuration_id=job_configuration.id,
    )

    db.add(step_configuration)
    db.commit()
    db.refresh(step_configuration)
    db.refresh(job_configuration)

    assert step_configuration.job_configuration_id == job_configuration.id
    assert step_configuration.points == 20
    assert step_configuration.job_tag == "prostate_v1_job"
    assert step_configuration.tag == "kidney_scan"

    assert len(job_configuration.provider_step_configurations) == 1
    assert step_configuration.job_tag == job_configuration.tag
    assert step_configuration.provider_step_configuration_name == "Kidney Scan"


def test_create_step_configuration_missing_job_configuration_id(db):
    step_configuration = models.StepConfiguration(
        job_tag="prostate_v1_job",
        tag="kidney_scan",
        provider_step_configuration_name="Kidney Scan",
        points=20,
    )

    db.add(step_configuration)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as exc:
        db.commit()
    assert isinstance(exc.value.orig, psycopg2.errors.NotNullViolation)
    assert "job_configuration_id" in str(exc.value.orig)


def test_create_step_configuration_missing_points(db, random_provider_user):
    job_configuration = models.JobConfiguration(
        tag="prostate_v1_job",
        provider_job_configuration_name="Prostate Job",
        provider_id=random_provider_user.id,
    )

    db.add(job_configuration)
    db.commit()
    db.refresh(job_configuration)

    step_configuration = models.StepConfiguration(
        job_tag="prostate_v1_job",
        tag="kidney_scan",
        provider_step_configuration_name="Kidney Scan",
        job_configuration_id=job_configuration.id,
    )

    db.add(step_configuration)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as exc:
        db.commit()

    assert isinstance(exc.value.orig, psycopg2.errors.NotNullViolation)
    assert "points" in str(exc.value.orig)


def test_create_step_configuration_with_wrong_job_configuration_id(
    db, random_provider_user
):
    job_configuration = models.JobConfiguration(
        tag="prostate_v1_job",
        provider_job_configuration_name="Prostate Job",
        provider_id=random_provider_user.id,
    )

    db.add(job_configuration)
    db.commit()
    db.refresh(job_configuration)

    step_configuration = models.StepConfiguration(
        job_tag="prostate_v1_job",
        tag="kidney_scan",
        provider_step_configuration_name="Kidney Scan",
        job_configuration_id=69,
        points=5,
    )

    db.add(step_configuration)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as exc:
        db.commit()

    assert isinstance(exc.value.orig, psycopg2.errors.ForeignKeyViolation)
