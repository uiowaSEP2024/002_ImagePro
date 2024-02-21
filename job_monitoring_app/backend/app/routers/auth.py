from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ...app.dependencies import get_db, get_current_user_from_token
from ...app.schemas.tokens import Token
from ...app.services.users import authenticate_user
from ...config import config
from ..internal.security import create_access_token

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
            expires_minutes=config.settings.access_token_expire_minutes,
            secret=config.settings.secret_key,
            algorithm=config.settings.algorithm,
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
def login(user=Depends(get_current_user_from_token)):  # noqa: F811
    return {"user": user, "message": "already logged in!"}
