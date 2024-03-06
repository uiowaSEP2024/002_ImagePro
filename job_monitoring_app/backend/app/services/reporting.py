import json
from datetime import datetime

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import models, schemas


def get_reporting_events(
    db: Session, provider_id: int, start_date: float, end_date: float
) -> list[dict]:
    """
    Retrieves and returns a list of reporting events from a database.

    Args:
        db (Session): The database session.
        provider_id (int): The ID of the provider.
        start_date (float): The start date as a timestamp.
        end_date (float): The end date as a timestamp.

    Returns:
        final (list[dict]): A list of all matching events from the database, serialized and formatted.

    The function begins by converting the start_date and end_date from float timestamps to datetime objects.
    This is done to facilitate the subsequent database query.

    A SQL query is then constructed using SQLAlchemy's ORM. The query is designed to select from the Event model
    and join with the Study, StudyConfiguration, and StepConfiguration models. The join is based on the relationships
    defined in the models. The query also includes filters to only select events where the Study's provider_id matches
    the provided provider_id and the Event's created_at date is within the range of start_date and end_date.

    The query is then executed using the all() method, which returns all results that match the query. The results
    are stored in the results variable.

    Each result is then serialized and formatted into a dictionary, which is added to the final list that is returned.
    """
    end_date = datetime.fromtimestamp(end_date)
    start_date = datetime.fromtimestamp(start_date)

    query = (
        db.query(
            models.Event,
            models.Study,
            models.StudyConfiguration,
            models.StepConfiguration,
        )
        .select_from(models.Event)
        .join(models.Study, models.Event.study)
        .join(models.StudyConfiguration, models.Study.study_configuration)
        .join(models.StepConfiguration, models.Event.step_configuration)
        .filter(models.Study.provider_id == provider_id)
        .filter(models.Event.created_at >= start_date)
        .filter(models.Event.created_at <= end_date)
    )

    results = query.all()

    def serialized(model: BaseModel, exclude=None):
        """
        Serializes a model into a JSON string, then loads it back into a dictionary.

        Args:
            model (BaseModel): The model to serialize.
            exclude (set, optional): A set of keys to exclude from the serialized model. Defaults to None.

        Returns:
            dict: The serialized model as a dictionary.
        """
        exclude = exclude if exclude else set()
        return json.loads(model.json(encoder=str, exclude=exclude))

    final: list[dict] = [
        {
            # For each key-value pair in the serialized Event object,
            # add a new key-value pair to the dictionary where the key is prefixed with "event."
            **{
                k + ".event": v
                for k, v in serialized(schemas.EventPure.from_orm(event)).items()
            },
            # Do the same for the StudyConfiguration object, but prefix the keys with "study_configuration."
            **{
                k + ".study_configuration": v
                for k, v in serialized(
                    schemas.StudyConfiguration.from_orm(study_configuration),
                ).items()
            },
            # Do the same for the Study object, but prefix the keys with "study."
            **{
                k + ".study": v
                for k, v in serialized(schemas.StudyPure.from_orm(study)).items()
            },
            # Do the same for the StepConfiguration object, but prefix the keys with "step_configuration."
            **{
                k + ".step_configuration": v
                for k, v in serialized(
                    schemas.StepConfiguration.from_orm(step_configuration)
                ).items()
            },
        }
        # Do this for each tuple in the results list.
        for event, study, study_configuration, step_configuration in results
    ]

    return final
