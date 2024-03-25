from app.dependencies import get_db, get_current_user_from_token
from app import schemas, services
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Union


router = APIRouter()
router.tags = ["users"]


@router.post("/users/", response_model=schemas.User)
def create_user(
    user: Union[
        schemas.UserCreate.schemas.UserHospitalCreate, schemas.UserProviderCreate
    ],
    db: Session = Depends(get_db),
):
    if user.role == "hospital":
        return services.create_hospital_user(db=db, user=user)
    elif user.role == "provider":
        return services.create_provider_user(db=db, user=user)
    else:
        return services.create_user(db=db, user=user)


@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user_from_token),
):
    db_user = services.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
