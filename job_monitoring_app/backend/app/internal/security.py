from datetime import datetime
from datetime import timedelta
from jose import jwt


def create_access_token(
    data: dict, expires_minutes: float, secret: str, algorithm: str
) -> str:
    """
    Creates an access token

    :param data: Data to be encoded in the token
    :param expires_minutes: Time in minutes
    :param secret: Secret key
    :param algorithm: Algorithm to be used for encoding the token

    :return: Encoded token
    """
    # This seems weird for it to have its very own file but it's not worth the effort to refactor
    to_encode = data.copy()
    expires_delta = timedelta(minutes=float(expires_minutes))

    expire_time = datetime.utcnow() + expires_delta

    to_encode.update({"exp": expire_time})

    encoded_jwt = jwt.encode(to_encode, secret, algorithm=algorithm)
    return encoded_jwt
