from typing import List

from app.dependencies import get_db
from app import schemas, services
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


router = APIRouter()
router.tags = ["providers"]


@router.get("/providers", response_model=List[schemas.Provider])
def get_providers(
    db: Session = Depends(get_db),
):
    return services.get_all_providers(db)


@router.get("/providers/{provider_id}", response_model=schemas.Provider)
def get_provider(
    provider_id: int,
    db: Session = Depends(get_db),
):
    return services.get_provider_by_id(db, provider_id=provider_id)
