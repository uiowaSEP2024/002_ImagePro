from typing import Dict
from typing import Optional
from fastapi import Request
from fastapi import Security, Depends, HTTPException
from fastapi import status
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.api_key import APIKeyHeader
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED
from starlette.status import HTTP_403_FORBIDDEN

from app import services
from app.models import User
from app.schemas.user import UserRoleEnum
from app.services.users import get_user_by_email
from config import config

API_KEY_HEADER_NAME = "x-api_key"


def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()


class OAuth2HttpCookieBearer(OAuth2):
    """
    Source: Adapted from FastAPI OAuth2PasswordBearer. Instead of getting authorization
    string from request header, instead gets it from cookie's "access_token" field.
    """

    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        authorization = request.cookies.get("access_token")
        scheme, param = get_authorization_scheme_param(authorization)

        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


oauth2_http_cookie_bearer_scheme = OAuth2HttpCookieBearer(tokenUrl="login")


def get_current_user_from_token(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_http_cookie_bearer_scheme),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:
        payload = jwt.decode(
            token, config.settings.secret_key, algorithms=[config.settings.algorithm]
        )
        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception

        user = get_user_by_email(email=email, db=db)

        if user is None:
            raise credentials_exception

        return user
    except JWTError:
        raise credentials_exception


get_api_key_from_header = APIKeyHeader(name=API_KEY_HEADER_NAME, auto_error=False)


def get_current_provider(user=Depends(get_current_user_from_token)) -> User:
    if user.role == UserRoleEnum.provider:
        return user

    raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Not authorized",
    )


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

    api_key = services.get_apikey_by_key(db, api_key_header_value)

    if not api_key or services.is_apikey_expired(api_key):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=INVALID_API_KEY_CREDENTIALS_UNAUTHORIZED,
        )

    return api_key.user
