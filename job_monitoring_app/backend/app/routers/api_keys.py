from ..dependencies import (
    get_db,
    get_user_from_api_key,
    API_KEY_HEADER_NAME,
    get_current_provider,
)
from .. import schemas, services
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()
router.tags = ["api-keys"]


# TODO: add current_user/authenticated_user dependency to ensure only
#   accessible by logged in user
# create API Key
@router.post("/api-keys", response_model=schemas.Apikey)
def generate_api_key(
    key: schemas.ApikeyCreate,
    user=Depends(get_current_provider),
    db: Session = Depends(get_db),
):
    return services.create_apikey_for_user(db, user.id, key=key)


# TODO: add current_user/authenticated_user dependency to ensure only
#   accessible by logged in user
# get all API keys for current user
@router.get("/api-keys", response_model=list[schemas.ApikeyPublic])
def read_apikeys(user=Depends(get_current_provider), db: Session = Depends(get_db)):
    return services.get_api_keys_for_user(db, user.id)


@router.post("/api-keys/{apikey_id}/expire", response_model=schemas.ApikeyPublic)
def expire_apikey(
    apikey_id: int, user=Depends(get_current_provider), db: Session = Depends(get_db)
):
    return services.expire_apikey_for_user(db, user.id, apikey_id)


@router.get(
    "/api-keys/protected",
    response_model=str,
    openapi_extra={API_KEY_HEADER_NAME: "your-api-key"},
)
def read_api_key_protected_route(user=Depends(get_user_from_api_key)):
    return "Authorized!"
