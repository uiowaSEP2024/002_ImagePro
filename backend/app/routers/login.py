from app.dependencies import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from app import schemas, services
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from datetime import timedelta
from ..internal.security import create_access_token
from fastapi import Response
from fastapi import Request
from app.services.utils import OAuth2PasswordBearerWithCookie
from app.schemas.tokens import Token
from app.services.users import authenticate_user, get_user_email
from fastapi import HTTPException
from fastapi import status
from jose import jwt
from config import settings
from jose import JWTError
from fastapi.responses import JSONResponse

router = APIRouter()
router.tags = ["login"]


@router.post("/login", response_model=Token)
def login_for_access_token(
    response: Response,
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    try:
        user = authenticate_user(form_data.username, form_data.password, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        response.set_cookie(
            key="access_token", value=f"Bearer {access_token}", httponly=True
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except:
        print("Server Error")
        # return {"access_token": "", "token_type": ""}
    # response.status_code = 200
    # response.body = {"access_token": access_token, "token_type": "bearer"}
    # return response


# oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/login/token")


# def get_current_user_from_token(
#     token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
# ):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#     )
#     try:
#         payload = jwt.decode(
#             token, settings.secret_key, algorithms=[settings.algorithm]
#         )
#         username: str = payload.get("sub")
#         print("username/email extracted is ", username)
#         if username is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
#     user = get_user_email(username=username, db=db)
#     if user is None:
#         raise credentials_exception
#     return user
