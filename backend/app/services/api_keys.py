from app import models,schemas
from app.internal import generate_apikey
from passlib.context import CryptContext
from pydantic import validate_arguments
from sqlalchemy.orm import Session

from .users import get_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_api_keys_for_user(db: Session, user_id: int):
    return get_user(db, user_id).api_keys


@validate_arguments(config=dict(arbitrary_types_allowed=True))
def get_user_from_api_key(db: Session, api_key: str):
    # TODO: only allow fetching for api keys that have not expired
    api_key = db.query(models.Apikey).filter(models.Apikey.key == api_key)
    if api_key.first():
        return api_key.one().user


def create_apikey_for_user(db: Session, user_id: int, key: schemas.ApikeyCreate):
    db_apikey = models.Apikey(key=generate_apikey(), user_id=user_id, note=key.note)

    db.add(db_apikey)
    db.commit()
    db.refresh(db_apikey)
    return db_apikey
