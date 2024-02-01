import json
from datetime import datetime, timedelta

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import models, schemas


def get_reporting_events(
    db: Session, provider_id: int, start_date: float, end_date: float
):
    end_date = datetime.fromtimestamp(end_date)
    start_date = datetime.fromtimestamp(start_date)

    print(end_date, start_date)

    query = (
        db.query(
            models.Event, models.Job, models.JobConfiguration, models.StepConfiguration
        )
        .select_from(models.Event)
        .join(models.Job, models.Event.job)
        .join(models.JobConfiguration, models.Job.job_configuration)
        .join(models.StepConfiguration, models.Event.step_configuration)
        .filter(models.Job.provider_id == provider_id)
        .filter(models.Event.created_at >= start_date)
        .filter(models.Event.created_at <= end_date)
    )

    results = query.all()

    def serialized(model: BaseModel, exclude=None):
        exclude = exclude if exclude else set()
        return json.loads(model.json(encoder=str, exclude=exclude))

    final = [
        {
            **{
                k + ".event": v
                for k, v in serialized(schemas.EventPure.from_orm(event)).items()
            },
            **{
                k + ".job_configuration": v
                for k, v in serialized(
                    schemas.JobConfiguration.from_orm(job_configuration),
                ).items()
            },
            **{
                k + ".job": v
                for k, v in serialized(schemas.JobPure.from_orm(job)).items()
            },
            **{
                k + ".step_configuration": v
                for k, v in serialized(
                    schemas.StepConfiguration.from_orm(step_configuration)
                ).items()
            },
        }
        for event, job, job_configuration, step_configuration in results
    ]

    return final
