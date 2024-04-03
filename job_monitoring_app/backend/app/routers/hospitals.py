from typing import List

from app import schemas, services
from app.dependencies import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()
router.tags = ["hospitals"]


@router.get("/hospitals", response_model=List[schemas.Hospital])
def get_hospitals(
    db: Session = Depends(get_db),
):
    return services.get_all_hospitals(db)


@router.get("/hospitals/{hospital_id}", response_model=schemas.Hospital)
def get_hospital(
    hospital_id: int,
    db: Session = Depends(get_db),
):
    return services.get_hospital_by_id(db, hospital_id=hospital_id)
