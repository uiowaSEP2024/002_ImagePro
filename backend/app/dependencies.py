from config.database import SessionLocal
from fastapi import Security, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_403_FORBIDDEN

from app import services
from fastapi.security.api_key import APIKeyHeader

API_KEY_HEADER_NAME = "x-api_key"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


get_api_key_from_header = APIKeyHeader(name=API_KEY_HEADER_NAME, auto_error=False)


INVALID_API_KEY_CREDENTIALS_MISSING = (
    f"Invalid credentials. Missing {API_KEY_HEADER_NAME} header"
)

INVALID_API_KEY_CREDENTIALS_UNAUTHORIZED = "Invalid credentials. Unauthorized"


async def get_user_from_api_key(
    api_key_header_value: str = Security(get_api_key_from_header),
    db: Session = Depends(get_db),
):
    if not api_key_header_value or api_key_header_value is None:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=INVALID_API_KEY_CREDENTIALS_MISSING,
        )

    user = services.get_user_from_api_key(db=db, api_key=api_key_header_value)

    if user:
        return user

    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN, detail=INVALID_API_KEY_CREDENTIALS_UNAUTHORIZED
    )
