import psycopg2.errors
import pytest
import sqlalchemy

from app import models


def test_delete_job_configuration_after_creating_study(
    db, random_provider_user, random_test_user
):
    job_configuration = models.JobConfiguration(
        tag="prostate_v1_job",
        name="Prostate Job",
        provider_id=random_provider_user.id,
        version="1.1",
    )

    db.add(job_configuration)
    db.commit()

    study = models.Study(
        provider_study_id="abc123",
        provider_study_name="kidneyV1",
        hospital_id=random_test_user.id,
        provider_id=random_provider_user.id,
        job_configuration_id=job_configuration.id,
    )

    db.add(study)
    db.commit()

    db.refresh(study)

    db.delete(job_configuration)
    db.commit()

    db.refresh(study)
    assert study is not None

    assert db.query(models.Study).get(study.id) is not None
    assert study.job_configuration_id is None


def test_create_study_with_configuration(db, random_test_user, random_provider_user):
    job_configuration = models.JobConfiguration(
        tag="prostate_v1_job",
        name="Prostate Job",
        provider_id=random_provider_user.id,
        version="1.1",
    )

    db.add(job_configuration)
    db.commit()

    study = models.Study(
        provider_study_id="abc123",
        provider_study_name="kidneyV1",
        hospital_id=random_test_user.id,
        provider_id=random_provider_user.id,
        job_configuration_id=job_configuration.id,
    )

    db.add(study)
    db.commit()

    db.refresh(study)

    assert isinstance(study, models.Study)
    assert study.hospital_id == random_test_user.id
    assert study.provider_study_id == "abc123"
    assert study.provider_study_name == "kidneyV1"
    assert study.job_configuration == job_configuration
    assert study.created_at is not None

    db.refresh(random_test_user)
    # Check that the customer user now has the correct jobs associated with them
    assert len(random_test_user.studies) == 1
    assert random_test_user.studies[0].provider_study_id == "abc123"
    assert random_test_user.studies[0].hospital_id == random_test_user.id

    db.refresh(random_provider_user)
    # Check that the provider user now has the correct jobs associated with them
    assert len(random_provider_user.provider_studies) == 1
    assert random_provider_user.provider_studies[0].provider_study_id == "abc123"
    assert (
        random_provider_user.provider_studies[0].provider_id == random_provider_user.id
    )
    assert (
        random_provider_user.provider_studies[0].job_configuration == job_configuration
    )

    assert random_provider_user.job_configurations[0] == job_configuration


def test_create_study_duplicate_provider_study_ids(
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

    study1 = models.Study(
        provider_study_id=duplicate_job_id,
        provider_study_name="kidneyV1",
        hospital_id=random_test_user.id,
        provider_id=random_provider_user.id,
        job_configuration=job_configuration,
    )

    db.add(study1)
    db.commit()

    study2 = models.Study(
        provider_study_id=duplicate_job_id,
        provider_study_name="kidneyV1",
        hospital_id=random_test_user.id,
        provider_id=random_provider_user.id,
        job_configuration=job_configuration,
    )

    db.add(study2)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as exc:
        db.commit()

    # Check for null violation and that column is part of the error message in the error
    assert isinstance(exc.value.orig, psycopg2.errors.UniqueViolation)
    assert (
        'violates unique constraint "studies_provider_id_provider_study_id_key"'
        in str(exc.value.orig)
    )


def test_create_study_missing_hospital_id(db, random_test_user, random_provider_user):
    job_configuration = models.JobConfiguration(
        tag="prostate_v1_job",
        name="Prostate Job",
        provider_id=random_provider_user.id,
        version="1.1",
    )

    db.add(job_configuration)
    db.commit()

    study = models.Study(
        provider_study_id="abc123",
        provider_study_name="kidneyV1",
        provider_id=random_provider_user.id,
        job_configuration=job_configuration,
    )

    db.add(study)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as exc:
        db.commit()

    # Check for null violation and that column is part of the error message in the error
    assert isinstance(exc.value.orig, psycopg2.errors.NotNullViolation)
    assert "hospital_id" in str(exc.value.orig)


def test_create_study_missing_provider_study_id(
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
    study = models.Study(
        provider_study_name="kidneyV1",
        hospital_id=random_test_user.id,
        provider_id=random_provider_user.id,
        job_configuration=job_configuration,
    )

    db.add(study)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as exc:
        db.commit()

    # Check for null violation and that column is part of the error message in the error
    assert isinstance(exc.value.orig, psycopg2.errors.NotNullViolation)
    assert "provider_study_id" in str(exc.value.orig)
