from app.dependencies import get_db
from app import schemas, services
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()
router.tags = ["api-keys"]


# create API Key
@router.post("/api-key", response_model=schemas.Apikey)
def generate_api_key(user_id: int, db: Session = Depends(get_db)):
    return services.create_apikey_for_user(db, user_id)


# get all API keys for current user
@router.get("/api-key", response_model=list[schemas.Apikey])
def read_apikeys(user_id: int, db: Session = Depends(get_db)):
    return services.get_user_apikeys(db, user_id)


@router.get("/api-key/protected", response_model=str)
def read_api_keys(api_key: int, db: Session = Depends(get_db)):
    return "Authorized!"
