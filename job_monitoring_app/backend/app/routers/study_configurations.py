from typing import Union, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, services
from app.dependencies import get_db
from app.dependencies import get_user_from_api_key, get_current_provider

router = APIRouter()
router.tags = ["study_configurations"]


@router.post("/study_configurations", response_model=schemas.StudyConfiguration)
def create_study(
    study_configuration: schemas.StudyConfigurationCreate,
    db: Session = Depends(get_db),
    provider=Depends(get_user_from_api_key),
):
    return services.create_study_configuration(
        db, provider_id=provider.id, study_configuration=study_configuration
    )


@router.get(
    "/study_configurations/{study_configuration_id}",
    response_model=schemas.StudyConfiguration,
)
def get_study_configuration_by_id(
    study_configuration_id: int,
    db: Session = Depends(get_db),
    provider=Depends(get_current_provider),
):
    study_configuration = services.get_study_configuration_by_id(
        db, study_configuration_id=study_configuration_id
    )

    if study_configuration is None:
        raise HTTPException(status_code=404, detail="Study not found")

    if provider.id not in [study_configuration.provider_id]:
        raise HTTPException(status_code=403, detail="Not allowed")

    return study_configuration


@router.get("/study_configurations/", response_model=List[schemas.StudyConfiguration])
def get_study_configurations_by_tag_and_version(
    tag: Union[str, None] = None,
    version: Union[str, None] = None,
    db: Session = Depends(get_db),
    provider=Depends(get_current_provider),
):
    # case 1: get specific configuration if both tag and version are provided
    should_get_specific_version_of_tag = tag and (
        isinstance(version, str) and version != "latest"
    )

    if should_get_specific_version_of_tag:
        return [
            services.get_study_configuration_by_composite_key(
                db, provider.id, tag, version
            )
        ]

    # case 2: get the latest study configuration for a specific tag
    should_get_latest_version_of_tag = tag and version == "latest"

    if should_get_latest_version_of_tag:
        return [services.get_study_configuration_by_tag(db, tag, provider.id)]

    # case 3: get all study configurations for a particular tag
    should_get_all_versions_of_tag = tag and version is None

    if should_get_all_versions_of_tag:
        return services.get_study_configurations_by_tag(db, tag, provider.id)

    # case 4: get latest version for all
    should_get_latest_versions_of_all_tags = tag is None and (
        version is None or version == "latest"
    )

    if should_get_latest_versions_of_all_tags:
        return services.get_list_of_latest_versions_for_all_study_configurations(
            db, provider.id
        )

    return services.get_list_of_latest_versions_for_all_study_configurations(
        db, provider.id
    )
