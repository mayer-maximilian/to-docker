from datetime import datetime, timedelta, timezone
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import HTTPBasic, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Optional
from zoneinfo import ZoneInfo

import database as db
from cache import invalidate_jwt_token, get_jwt_token
from passwords import verify_password

SECRET_KEY = 'foobar'  # TODO: store in K8S secret and fetch with os.getenv('SECRET_KEY')
LOCALTIME = ZoneInfo('Europe/Amsterdam')

router = APIRouter()

http_security = HTTPBasic()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/authenticate')
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE = 3  # hours


class CredentialsException(HTTPException):
    """The exception that is thrown when the credentials a user provides are not correct."""
    def __init__(self):
        super().__init__(status_code=401, detail='You shall not pass! - '
                                                 'Incorrect username or password or your token has expired',
                         headers={'WWW-Authenticate': 'Bearer'})


class UserDisabledException(HTTPException):
    """The exception that is thrown when the user that is used for authentication is disabled."""
    def __init__(self, message='Inactive user'):
        super().__init__(status_code=401, detail=message)


class NewUser(BaseModel):
    """Base model for a new user."""
    username: str
    email: str
    password: str


class User(BaseModel):
    """Base model for an existing user."""
    username: str
    disabled: Optional[bool] = False


class UserInDB(User):
    """Base model for a returned user."""
    hashed_password: str


class Token(BaseModel):
    """Base model for an authentication token."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Base model for authentication token data."""
    username: Optional[str] = None


def time_to_int(time_obj):
    """
        Returns an integer representation of the time object in milliseconds

        :param time_obj: time object to convert to an integer
        :return: integer representing the time in milliseconds
    """
    int_time = int(time_obj.microsecond / 1000) + int(time_obj.timestamp()) * 1000
    return int_time


def get_user(username: str):
    """
        Get a user by username.

        :param username: the username of the user
        :return: user if exists in the database
    """
    with db.Session() as session:
        user = db.users.find_user(session, username)
        if user:
            return UserInDB(**user)


def authenticate_user(username: str, password: str):
    """
        Authenticate a user.

        :param username: a username
        :param password: the unhashed password of the user
    """
    user = get_user(username)
    print(user)
    return user if user and verify_password(password, user.hashed_password) else False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = timedelta(minutes=15)):
    """
        Create an access token.

        :param data: data to include in the token
        :param expires_delta: the time until the token expires
        :return: access token
    """
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + expires_delta
    to_encode.update({'exp': time_to_int(expire)})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def validate_access_token(token):
    """
        Validate the currently active OAuth token by checking against the redis token blacklist.

        :param token: active token to validate
        :returns: bool whether the token is on the expired token blacklist
    """
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    exp_time = decoded_token['exp']
    int_now = time_to_int(datetime.now(tz=timezone.utc))
    if exp_time < int_now:
        return False

    return not bool(get_jwt_token(token))


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
        Get the user based on a token.

        :param token: the token for which to get the user
        :return: a user
    """
    if not validate_access_token(token):
        raise CredentialsException

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise CredentialsException
        token_data = TokenData(username=username)
    except JWTError:
        raise CredentialsException

    user = get_user(username=token_data.username)
    if user is None:
        raise CredentialsException
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
        Get the currently active user to check whether it is a user that was not disabled.

        :param current_user: the currently active user
        :return: current active user if not disabled
    """
    if current_user.disabled:
        raise UserDisabledException
    return current_user


@router.post('/authenticate', response_model=Token,
             summary='Authenticate to obtain a token for using in secured endpoints',
             status_code=200)
async def auth_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
        Function for the authentication endpoint. Takes data and creates an access token if the data checks out and
        the user has not been disabled.

        :param form_data: data containing the username and password for the login attempt
        :return: a dictionary containing the access token and the token type
    """
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        raise CredentialsException

    access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE)
    access_token = create_access_token(data={'sub': user.username}, expires_delta=access_token_expires)

    return {'access_token': access_token, 'token_type': 'bearer'}


@router.delete('/logout', dependencies=[Depends(get_current_user)],
               summary='Expire the current active OAuth2 token for secured endpoints',
               status_code=200)
async def expire_token(token: str = Depends(oauth2_scheme)):
    """
        Invalidate the currently active OAuth2 token for secured endpoints.

        :param token: current active token to expire
        :returns: confirmation message
    """
    int_now = time_to_int(datetime.now(tz=LOCALTIME))
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    invalidate_jwt_token(token, int((payload['exp']/1000) + 1 - (int_now/1000))) # Add a second for safety
    return {'message': f"Token {token} was successfully expired on {datetime.now(tz=LOCALTIME)}."}


@router.get('/check-login', dependencies=[Depends(get_current_user)], include_in_schema=False,
            summary='Check whether the provided token is still valid', status_code=200)
async def check_login(token: str = Depends(oauth2_scheme)):
    if not validate_access_token(token):
        raise CredentialsException
    return {'message': 'Login validated'}
