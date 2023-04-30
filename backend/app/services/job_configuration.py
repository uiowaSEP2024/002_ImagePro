from sqlalchemy.orm import Session

from app import models


def get_job_configuration_by_tag(db: Session, tag: str):
    return (
        db.query(models.JobConfiguration)
        .filter(models.JobConfiguration.tag == tag)
        .first()
    )
