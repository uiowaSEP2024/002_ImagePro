from app.dependencies import get_db, get_user_from_api_key
from app import schemas, services
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

router = APIRouter()
router.tags = ["api-keys"]


# TODO: add current_user/authenticated_user dependency to ensure only
#   accessible by logged in user
# create API Key
@router.post("/api-keys", response_model=schemas.Apikey)
def generate_api_key(body: schemas.ApiKeyCreateRequest, db: Session = Depends(get_db)):
    return services.create_apikey_for_user(db, body.user_id)


# TODO: add current_user/authenticated_user dependency to ensure only
#   accessible by logged in user
# get all API keys for current user
@router.get("/api-keys", response_model=list[schemas.Apikey])
def read_apikeys(user_id: str, db: Session = Depends(get_db)):
    return services.get_api_keys_for_user(db, int(user_id))


@router.get("/api-keys/protected", response_model=str)
def read_api_key_protected_route(user=Depends(get_user_from_api_key)):
    print(user)
    return "Authorized!"
