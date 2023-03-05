from app.dependencies import get_db, get_current_user_from_token
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from app import schemas, services
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from datetime import timedelta
from ..internal.security import create_access_token
from fastapi import Response
from fastapi import Request
from app.schemas.tokens import Token
from app.services.users import get_user_by_email, authenticate_user
from fastapi import HTTPException
from fastapi import status
from jose import jwt
from config import settings
from jose import JWTError
from fastapi.responses import JSONResponse

router = APIRouter()
router.tags = ["auth"]


INCORRECT_USER_NAME_OR_PASSWORD = "Incorrect user name or password"


@router.post("/login", response_model=Token)
def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    try:
        user = authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=INCORRECT_USER_NAME_OR_PASSWORD,
            )

        access_token = create_access_token(
            data={"sub": user.email},
            expires_minutes=settings.access_token_expire_minutes,
            secret=settings.secret_key,
            algorithm=settings.algorithm,
        )

        response.set_cookie(
            key="access_token", value=f"Bearer {access_token}", httponly=True
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error",
        )


@router.post("/logout", response_model=str)
def logout(
    response: Response,
):
    response.set_cookie(key="access_token", value="", httponly=True)
    return "Logout successful!"


@router.get("/login", response_model=dict)
def login(user=Depends(get_current_user_from_token)):
    return {"user": user, "message": "already logged in!"}
