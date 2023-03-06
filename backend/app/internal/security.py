from datetime import datetime
from datetime import timedelta
from jose import jwt


def create_access_token(
    data: dict, expires_minutes: float, secret: str, algorithm: str
):
    to_encode = data.copy()
    expires_delta = timedelta(minutes=float(expires_minutes))

    expire_time = datetime.utcnow() + expires_delta

    to_encode.update({"exp": expire_time})

    encoded_jwt = jwt.encode(to_encode, secret, algorithm=algorithm)
    return encoded_jwt
