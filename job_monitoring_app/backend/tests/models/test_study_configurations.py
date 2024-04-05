import psycopg2.errors
import pytest
import sqlalchemy

from app import models


def test_create_study_configurtaion(db, random_provider):
    study_configuration = models.StudyConfiguration(
        tag="prostate_v1_study",
        name="Prostate Study",
        provider_id=random_provider.id,
        version="1.1",
    )

    db.add(study_configuration)
    db.commit()
    db.refresh(study_configuration)

    assert isinstance(study_configuration, models.StudyConfiguration)
    assert study_configuration.provider_id == random_provider.id
    assert study_configuration.tag == "prostate_v1_study"
    assert study_configuration.name == "Prostate Study"

    db.refresh(random_provider)
    assert len(random_provider.study_configurations) == 1
    assert random_provider.study_configurations[0].tag == "prostate_v1_study"
    assert random_provider.study_configurations[0].provider_id == random_provider.id


def test_duplicate_study_configuration_tag_and_version(db, random_provider):
    study_configuration1 = models.StudyConfiguration(
        tag="prostate_v1_study",
        name="Prostate Study",
        provider_id=random_provider.id,
        version="1.2.8",
    )
    db.add(study_configuration1)
    db.commit()

    study_configuration1 = models.StudyConfiguration(
        tag="prostate_v1_study",
        name="Prostate Study",
        provider_id=random_provider.id,
        version="1.2.8",
    )
    db.add(study_configuration1)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as exc:
        db.commit()

    assert isinstance(exc.value.orig, psycopg2.errors.UniqueViolation)
    assert (
        'violates unique constraint "study_configurations_provider_id_tag_version_key"'
        in str(exc.value.orig)
    )


def test_missing_tag(db, random_provider):
    study_configuration = models.StudyConfiguration(
        name="Prostate Study",
        provider_id=random_provider.id,
        version="1.2.1",
    )
    db.add(study_configuration)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as exc:
        db.commit()

    assert isinstance(exc.value.orig, psycopg2.errors.NotNullViolation)
    assert "tag" in str(exc.value.orig)


#
def test_create_study_missing_study_configuration_name(db, random_provider_user):
    study_configuration1 = models.StudyConfiguration(
        tag="prostate_v1_study", provider_id=random_provider_user.id, version="1.2.1"
    )
    db.add(study_configuration1)
    with pytest.raises(sqlalchemy.exc.IntegrityError) as exc:
        db.commit()

    # Check for null violation and that column is part of the error message in the error
    assert isinstance(exc.value.orig, psycopg2.errors.NotNullViolation)
    assert "name" in str(exc.value.orig)


def test_create_study_missing_provider_id(db):
    study_configuration1 = models.StudyConfiguration(
        tag="prostate_v1_study",
        name="Prostate Study",
        version="1.2.1",
    )
    db.add(study_configuration1)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as exc:
        db.commit()

        # Check for null violation and that column is part of the error message in the error
    assert isinstance(exc.value.orig, psycopg2.errors.NotNullViolation)
    assert "provider_id" in str(exc.value.orig)


#
def test_create_study_missing_version(db, random_provider):
    study_configuration = models.StudyConfiguration(
        tag="prostate_v1_study",
        name="Prostate Study",
        provider_id=random_provider.id,
    )
    db.add(study_configuration)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as exc:
        db.commit()

    assert isinstance(exc.value.orig, psycopg2.errors.NotNullViolation)
    assert "version" in str(exc.value.orig)
