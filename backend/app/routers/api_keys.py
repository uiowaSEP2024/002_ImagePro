from app.dependencies import (
    get_db,
    get_user_from_api_key,
    API_KEY_HEADER_NAME,
    get_current_user_from_token,
)
from app import schemas, services
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

router = APIRouter()
router.tags = ["api-keys"]


# TODO: add current_user/authenticated_user dependency to ensure only
#   accessible by logged in user
# create API Key
@router.post("/api-keys", response_model=schemas.Apikey)
def generate_api_key(
    user=Depends(get_current_user_from_token), db: Session = Depends(get_db)
):
    return services.create_apikey_for_user(db, user.id)


# TODO: add current_user/authenticated_user dependency to ensure only
#   accessible by logged in user
# get all API keys for current user
@router.get("/api-keys", response_model=list[schemas.Apikey])
def read_apikeys(
    user=Depends(get_current_user_from_token), db: Session = Depends(get_db)
):
    return services.get_api_keys_for_user(db, user.id)


@router.get(
    "/api-keys/protected",
    response_model=str,
    openapi_extra={API_KEY_HEADER_NAME: "your-api-key"},
)
def read_api_key_protected_route(user=Depends(get_user_from_api_key)):
    print(user)
    return "Authorized!"
