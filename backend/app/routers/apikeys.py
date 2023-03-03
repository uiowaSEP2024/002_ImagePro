from app.dependencies import get_db
from app import schemas, services
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()
router.tags = ["apikeys"]


# create API Key
@router.post("/apikey", response_model=schemas.Apikey)
def generate_apikey(user_id: int, db: Session = Depends(get_db)):
    return services.create_apikey_for_user(db, user_id)


# get all API keys for current user
@router.get("/apikey", response_model=list[schemas.Apikey])
def read_apikeys(user_id: int, db: Session = Depends(get_db)):
    return services.get_user_apikeys(db, user_id)
