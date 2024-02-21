from fastapi import HTTPException
from sqlalchemy import asc
from starlette import status

from app import models, schemas
from app.internal import generate_apikey
from passlib.context import CryptContext
from pydantic import validate_arguments
from sqlalchemy.orm import Session

from datetime import datetime


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_api_keys_for_user(db: Session, user_id: int) -> list[models.Apikey]:
    """
    Get all api keys for a user

    Args:
        db (Session): SQLAlchemy session
        user_id (int): User id
    Returns:
        List[models.Apikey]: List of api keys
    """
    return (
        db.query(models.Apikey)
        .order_by(asc(models.Apikey.created_at))
        .filter(models.Apikey.user_id == user_id)
        .all()
    )


def get_apikey_by_id(db: Session, apikey_id: int) -> models.Apikey:
    """
    Get api key by id

    Args:
        db (Session): SQLAlchemy session
        apikey_id (int): Api key id
    Returns:
        models.Apikey: Api key

    """
    return db.query(models.Apikey).get(apikey_id)


def get_apikey_by_key(db: Session, key: str) -> models.Apikey:
    """ "
    Get api key by key

    Args:
        db (Session): SQLAlchemy session
        key (str): Api key
    Returns:
        models.Apikey: Api key
    """
    results = db.query(models.Apikey).filter(models.Apikey.key == key).all()
    assert len(results) <= 1, "Encountered duplicate api keys"
    return results[0] if len(results) == 1 else None


def is_apikey_expired(api_key: models.Apikey) -> bool:
    """
    Check if api key is expired

    Args:
        api_key (models.Apikey): Api key
    Returns:
        bool: True if expired, False otherwise
    """
    return (
        isinstance(api_key.expires_at, datetime)
        and api_key.expires_at.timestamp() <= datetime.now().timestamp()
    )


def expire_apikey_for_user(db: Session, user_id: int, id: int) -> models.Apikey:
    """
    Expire an api key for a user

    Args:
        db (Session): SQLAlchemy session
        user_id (int): User id
        id (int): Api key id
    Returns:
        models.Apikey: Expired api key
    """
    api_key = get_apikey_by_id(db, id)

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


# TODO: Figure out what the validate_arguments decorator is doing
@validate_arguments(config=dict(arbitrary_types_allowed=True))
def get_user_from_apikey_key(db: Session, key: str) -> models.User:
    """
    Get user from api key

    Args:
        db (Session): SQLAlchemy session
        key (str): Api key
    Returns:
        models.User: User
    """
    # TODO: only allow fetching for api keys that have not expired
    api_key = get_apikey_by_key(db, key)

    if api_key:
        return api_key.user


def create_apikey_for_user(
    db: Session, user_id: int, key: schemas.ApikeyCreate
) -> models.Apikey:
    """
    Create an api key for a user

    Args:
        db (Session): SQLAlchemy session
        user_id (int): User id
        key (schemas.ApikeyCreate): Api key

    Returns:
        models.Apikey: Created api key
    """
    db_apikey = models.Apikey(key=generate_apikey(), user_id=user_id, note=key.note)

    db.add(db_apikey)
    db.commit()
    db.refresh(db_apikey)
    return db_apikey
