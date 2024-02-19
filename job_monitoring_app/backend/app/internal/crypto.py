from passlib.context import CryptContext
import secrets

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


API_KEY_LENGTH = 20


def generate_apikey():
    return secrets.token_urlsafe(API_KEY_LENGTH)
