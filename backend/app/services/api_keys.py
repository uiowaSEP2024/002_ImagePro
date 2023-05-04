from fastapi import HTTPException
from sqlalchemy import asc
from starlette import status

from app import models, schemas
from app.internal import generate_apikey
from passlib.context import CryptContext
from pydantic import validate_arguments
from sqlalchemy.orm import Session

from datetime import datetime

from .users import get_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_api_keys_for_user(db: Session, user_id: int):
    return (
        db.query(models.Apikey)
        .order_by(asc(models.Apikey.created_at))
        .filter(models.Apikey.user_id == user_id)
        .all()
    )


def get_apikey(db: Session, apikey_id: int) -> models.Apikey:
    return db.query(models.Apikey).get(apikey_id)


def is_apikey_expired(api_key: models.Apikey):
    return (
        isinstance(api_key.expires_at, datetime)
        and api_key.expires_at.timestamp() <= datetime.now().timestamp()
    )


def expire_apikey_for_user(db: Session, user_id: int, id: int):
    api_key = get_apikey(db, id)

    if api_key.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"msg": "Not Allowed"},
        )

    if is_apikey_expired(api_key):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"msg": "Cannot expire already expired key"},
        )

    api_key.expires_at = datetime.now()
    db.add(api_key)
    db.commit()
    db.refresh(api_key)

    return api_key


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
