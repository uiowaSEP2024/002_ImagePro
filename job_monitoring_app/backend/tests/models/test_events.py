import psycopg2.errors
import pytest
import sqlalchemy

from app import models


def test_create_event(db, random_hospital, random_provider):

    study = models.Study(
        provider_study_id="abc123",
        provider_study_name="kidneyV1",
        hospital_id=random_hospital.id,
        provider_id=random_provider.id,
    )
    db.add(study)
    db.commit()
    db.refresh(study)

    # Create events for the study

    event = models.Event(
        study_id=study.id,
        name="Scanning Kidney",
        kind="Pending",
        event_metadata={"unofficial": "Yes"},
    )

    db.add(event)
    db.commit()
    db.refresh(event)
    db.refresh(study)

    assert event.study_id == study.id
    assert event.kind == "Pending"
    assert event.name == "Scanning Kidney"
    assert event.event_metadata == {"unofficial": "Yes"}
    assert event.created_at is not None

    assert len(study.events) == 1
    assert event.study.id == study.id


def test_create_event_missing_study_id(db):
    event = models.Event(name="Scanning Kidney", kind="Pending")

    db.add(event)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as exc:
        db.commit()

    assert isinstance(exc.value.orig, psycopg2.errors.NotNullViolation)
    assert "study_id" in str(exc.value.orig)


def test_create_study_missing_kind(db, random_hospital, random_provider):
    study = models.Study(
        provider_study_name="kidneyV1",
        hospital_id=random_hospital.id,
        provider_id=random_provider.id,
    )

    db.add(study)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as exc:
        db.commit()

    # Check for null violation and that column is part of the error message in the error
    assert isinstance(exc.value.orig, psycopg2.errors.NotNullViolation)
    assert "provider_study_id" in str(exc.value.orig)


def test_create_study_missing_provider_study_name(db, random_hospital, random_provider):
    study = models.Study(
        provider_study_id="abc123",
        provider_study_name="kidneyV1",
        hospital_id=random_hospital.id,
        provider_id=random_provider.id,
    )

    db.add(study)
    db.commit()
    db.refresh(study)

    # Create events for the study

    event = models.Event(study_id=study.id, name="Scanning Kidney")

    db.add(event)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as exc:
        db.commit()

    assert isinstance(exc.value.orig, psycopg2.errors.NotNullViolation)
    assert "kind" in str(exc.value.orig)


def test_create_event_for_step(
    db,
    random_hospital,
    random_provider,
    random_study_configuration_factory,
):
    study_configuration = random_study_configuration_factory.get(num_steps=1)

    study = models.Study(
        provider_study_id="abc123",
        provider_study_name="kidneyV1",
        hospital_id=random_hospital.id,
        provider_id=random_provider.id,
        study_configuration_id=study_configuration.id,
    )

    db.add(study)
    db.commit()
    db.refresh(study)

    # Create events for the study

    event = models.Event(
        study_id=study.id,
        name="Scanning Kidney",
        kind="Pending",
        step_configuration_id=study_configuration.step_configurations[0].id,
    )

    db.add(event)
    db.commit()
    db.refresh(event)
    db.refresh(study)

    assert event.step_configuration_id == study_configuration.step_configurations[0].id
