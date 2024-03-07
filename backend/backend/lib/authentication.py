from __future__ import annotations
from datetime import datetime, timezone, timedelta
from typing import Annotated, Dict, Final, Literal
from pydantic import BaseModel, EmailStr

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHashError
from joserfc import jwt
from joserfc.jwk import OKPKey
from joserfc.errors import BadSignatureError

from backend.config import JWT_ENCRYPTION_ALGORITHM
from backend.secrets.key import get_key
from backend.controller_instance import controller
from backend.definitions.user import User
from backend.definitions.course import Course

SECRET_KEY: Final[OKPKey] = get_key()
JWT_HEADER: Final[Dict] = {"alg": JWT_ENCRYPTION_ALGORITHM}
TOKEN_URL: Final[str] = "login"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)
password_hasher = PasswordHasher()


class Token(BaseModel):
    access_token: str
    token_type: str


class RegisterPostData(BaseModel):
    type: Literal["user", "teacher"]
    name: str
    email: EmailStr
    password: str


def verify_password(plain_password, correct_hash):
    try:
        password_hasher.verify(hash=correct_hash, password=plain_password)
        return True
    except VerifyMismatchError:
        return False
    except InvalidHashError:
        return False


def get_password_hash(password):
    password_hash = password_hasher.hash(password)
    return password_hash


def authenticate_user(email: EmailStr, password: str):
    user = controller.search_user_by_email(email)
    if user is None:
        return None
    if not verify_password(password, user.get_hashed_password()):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    payload = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    payload.update({"exp": expire})
    encoded_jwt = jwt.encode(
        JWT_HEADER, payload, SECRET_KEY, algorithms=[JWT_ENCRYPTION_ALGORITHM]
    )
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        decoded_token = jwt.decode(
            token, SECRET_KEY, algorithms=[JWT_ENCRYPTION_ALGORITHM]
        )
        payload = decoded_token.claims
        email: EmailStr = payload.get("sub", None)
        if email is None:
            raise credentials_exception
        # token_data = TokenData(username=username)
    except BadSignatureError as exc:
        raise credentials_exception from exc

    if email is None:
        raise credentials_exception from None
    user = controller.search_user_by_email(email)
    if user is None:
        raise credentials_exception
    return user
