from passlib.context import CryptContext
import secrets

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    """
    Verifies the password
    :param plain_password: Password in plain text
    :param hashed_password: Password in hashed form
    :return: True if the password is correct, False otherwise

    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    Returns the hashed password
    :param password: Password in plain text
    :return: Password in hashed form
    """
    return pwd_context.hash(password)


API_KEY_LENGTH = 20


def generate_apikey():
    """
    Generates a random API key
    :return: Random API key
    """
    return secrets.token_urlsafe(API_KEY_LENGTH)
