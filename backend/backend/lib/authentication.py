from datetime import datetime, timezone, timedelta
from typing import Annotated, Dict, Final
from pydantic import BaseModel

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from joserfc import jwt
from joserfc.jwk import OKPKey

from backend.config import JWT_ENCRYPTION_ALGORITHM
from backend.secrets.key import get_key


SECRET_KEY: Final[OKPKey] = get_key()
JWT_HEADER: Final[Dict] = {"alg": JWT_ENCRYPTION_ALGORITHM}
TOKEN_URL: Final[str] = 'token'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

class User(BaseModel):
    username: str
    full_name: str | None = None
    email: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(db, username: str, password: str) -> UserInDB | bool:
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    payload = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    payload.update({"exp": expire})
    encoded_jwt = jwt.encode(JWT_HEADER, payload, SECRET_KEY, algorithms=[JWT_ENCRYPTION_ALGORITHM])
    return encoded_jwt


# def fake_decode_token(token):
#     # This doesn't provide any security at all
#     # Check the next version
#     user = get_user(fake_users_db, token)
#     return user


# def fake_hash_password(password: str):
#     return "fakehashed" + password


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ENCRYPTION_ALGORITHM])
        payload = decoded_token.claims
        username: str = payload.get("sub", None)
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except Exception as exc:
        raise credentials_exception from exc

    if token_data.username is None:
        raise credentials_exception from None
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
