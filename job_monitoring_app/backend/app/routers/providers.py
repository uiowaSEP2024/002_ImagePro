from typing import List

from app import schemas, services
from app.dependencies import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()
router.tags = ["providers"]


@router.get("/providers", response_model=List[schemas.Provider])
def get_providers(
    db: Session = Depends(get_db),
):
    return services.get_all_providers(db)
