import psycopg2.errors
import pytest
import sqlalchemy

from app import models


def test_create_metatdata_configuratons(db, random_provider_user):
    job_configuration = models.JobConfiguration(
        tag="prostate_v1_job",
        name="Prostate Job",
        provider_id=random_provider_user.id,
        version="1.2.1",
    )

    db.add(job_configuration)
    db.commit()
    db.refresh(job_configuration)

    step_configuration = models.StepConfiguration(
        tag="kidney_scan",
        name="Kidney Scan",
        points=20,
        job_configuration_id=job_configuration.id,
    )

    db.add(step_configuration)
    db.commit()

    metadata_configuration = models.MetadataConfiguration(
        field_name="Protein Density",
        field_type="Integer",
        field_value="50",
        field_units="mg",
        step_configuration_id=step_configuration.id,
    )

    db.add(metadata_configuration)
    db.commit()

    db.refresh(metadata_configuration)
    db.refresh(step_configuration)
    db.refresh(job_configuration)

    assert (
        metadata_configuration.job_tag
        == step_configuration.job_tag
        == job_configuration.tag
    )
    assert metadata_configuration.field_name == "Protein Density"
    assert metadata_configuration.field_type == "Integer"
    assert metadata_configuration.field_value == "50"
    assert metadata_configuration.field_units == "mg"
    assert metadata_configuration.step_configuration_id == step_configuration.id
    assert (
        job_configuration.step_configurations[0].provider_metadata_configurations[0]
        == metadata_configuration
    )
    assert (
        len(job_configuration.step_configurations[0].provider_metadata_configurations)
        == 1
    )


def test_create_metadata_configuration_nonexistent_step_configuation_id(
    db, random_provider_user
):
    job_configuration = models.JobConfiguration(
        tag="prostate_v1_job",
        name="Prostate Job",
        provider_id=random_provider_user.id,
        version="1.2.1",
    )

    db.add(job_configuration)
    db.commit()
    db.refresh(job_configuration)

    step_configuration = models.StepConfiguration(
        tag="kidney_scan",
        name="Kidney Scan",
        points=20,
        job_configuration_id=job_configuration.id,
    )

    db.add(step_configuration)
    db.commit()

    metadata_configuration = models.MetadataConfiguration(
        field_name="Protein Density",
        field_type="Integer",
        field_units="mg",
        field_value="50",
        step_configuration_id=25,
    )

    db.add(metadata_configuration)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as exc:
        db.commit()
    assert isinstance(exc.value.orig, psycopg2.errors.ForeignKeyViolation)
    assert "step_configuration_id" in str(exc.value.orig)


def test_create_metadata_configuration_missing_step_configuation_id(
    db, random_provider_user
):
    job_configuration = models.JobConfiguration(
        tag="prostate_v1_job",
        name="Prostate Job",
        provider_id=random_provider_user.id,
        version="1.2.1",
    )

    db.add(job_configuration)
    db.commit()
    db.refresh(job_configuration)

    step_configuration = models.StepConfiguration(
        tag="kidney_scan",
        name="Kidney Scan",
        points=20,
        job_configuration_id=job_configuration.id,
    )

    db.add(step_configuration)
    db.commit()

    metadata_configuration = models.MetadataConfiguration(
        field_name="Protein Density",
        field_type="Integer",
        field_value="50",
        field_units="mg",
    )

    db.add(metadata_configuration)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as exc:
        db.commit()

    assert isinstance(exc.value.orig, psycopg2.errors.NotNullViolation)
    assert "step_configuration_id" in str(exc.value.orig)


def test_create_metadata_configuration_missing_value(db, random_provider_user):
    job_configuration = models.JobConfiguration(
        tag="prostate_v1_job",
        name="Prostate Job",
        provider_id=random_provider_user.id,
        version="1.2.1",
    )

    db.add(job_configuration)
    db.commit()
    db.refresh(job_configuration)

    step_configuration = models.StepConfiguration(
        tag="kidney_scan",
        name="Kidney Scan",
        points=20,
        job_configuration_id=job_configuration.id,
    )

    db.add(step_configuration)
    db.commit()

    metadata_configuration = models.MetadataConfiguration(
        field_name="Protein Density",
        field_type="Integer",
        field_units="mg",
        step_configuration_id=step_configuration.id,
    )

    db.add(metadata_configuration)

    with pytest.raises(sqlalchemy.exc.IntegrityError) as exc:
        db.commit()

    assert isinstance(exc.value.orig, psycopg2.errors.NotNullViolation)
    assert "field_value" in str(exc.value.orig)
