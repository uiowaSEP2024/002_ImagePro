import psycopg2.errors
import pytest
import sqlalchemy

from app import models


def test_create_step_configuration(db, random_provider_user):
    study_configuration = models.StudyConfiguration(
        tag="prostate_v1_study",
        name="Prostate Study",
        provider_id=random_provider_user.id,
        version="1.2.1",
    )

    db.add(study_configuration)
    db.commit()
    db.refresh(study_configuration)

    step_configuration = models.StepConfiguration(
        tag="kidney_scan",
        name="Kidney Scan",
        points=20,
        study_configuration_id=study_configuration.id,
    )

    db.add(step_configuration)
    db.commit()
    db.refresh(step_configuration)
    db.refresh(study_configuration)

    assert step_configuration.study_configuration_id == study_configuration.id
    assert step_configuration.points == 20
    assert step_configuration.tag == "kidney_scan"

    assert len(study_configuration.step_configurations) == 1
    assert step_configuration.name == "Kidney Scan"
    assert study_configuration.step_configurations[0].tag == "kidney_scan"


def test_create_step_configuration_missing_study_configuration_id(
    db, random_provider_user
):
    step_configuration = models.StepConfiguration(
        tag="kidney_scan",
        name="Kidney Scan",
        points=20,
    )

    db.add(step_configuration)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as exc:
        db.commit()
    assert isinstance(exc.value.orig, psycopg2.errors.NotNullViolation)
    assert "study_configuration_id" in str(exc.value.orig)


def test_create_step_configuration_missing_points(db, random_provider_user):
    study_configuration = models.StudyConfiguration(
        tag="prostate_v1_study",
        name="Prostate Study",
        provider_id=random_provider_user.id,
        version="1.2.1",
    )

    db.add(study_configuration)
    db.commit()
    db.refresh(study_configuration)

    step_configuration = models.StepConfiguration(
        tag="kidney_scan",
        name="Kidney Scan",
        study_configuration_id=study_configuration.id,
    )

    db.add(step_configuration)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as exc:
        db.commit()

    assert isinstance(exc.value.orig, psycopg2.errors.NotNullViolation)
    assert "points" in str(exc.value.orig)


def test_create_step_configuration_with_wrong_study_configuration_id(
    db, random_provider_user
):
    study_configuration = models.StudyConfiguration(
        tag="prostate_v1_study",
        name="Prostate Study",
        provider_id=random_provider_user.id,
        version="1.2.1",
    )

    db.add(study_configuration)
    db.commit()
    db.refresh(study_configuration)

    step_configuration = models.StepConfiguration(
        tag="kidney_scan",
        name="Kidney Scan",
        study_configuration_id=69,
        points=5,
    )

    db.add(step_configuration)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as exc:
        db.commit()

    assert isinstance(exc.value.orig, psycopg2.errors.ForeignKeyViolation)


def test_duplicate_step_configuration_tag(db, random_provider_user):
    study_configuration1 = models.StudyConfiguration(
        tag="prostate_v1_study",
        name="Prostate Study",
        provider_id=random_provider_user.id,
        version="1.2.8",
    )
    db.add(study_configuration1)
    db.commit()

    step_configuration = models.StepConfiguration(
        tag="kidney_scan",
        name="Kidney Scan",
        study_configuration_id=study_configuration1.id,
        points=5,
    )

    db.add(step_configuration)
    db.commit()

    step_configuration2 = models.StepConfiguration(
        tag="kidney_scan",
        name="Another Kidney Scan",
        study_configuration_id=study_configuration1.id,
        points=5,
    )

    db.add(step_configuration2)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as exc:
        db.commit()

    assert isinstance(exc.value.orig, psycopg2.errors.UniqueViolation)
    assert (
        'violates unique constraint "step_configurations_study_configuration_id_tag_key"'
        in str(exc.value.orig)
    )
