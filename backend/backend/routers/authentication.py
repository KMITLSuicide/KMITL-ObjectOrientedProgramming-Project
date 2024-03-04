from __future__ import annotations
from datetime import timedelta
from enum import Enum
from typing import Annotated, List
from fastapi import Body, Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from backend.definitions.user import Teacher, User
from backend.config import ACCESS_TOKEN_EXPIRE_MINUTES
from backend.lib.authentication import TOKEN_URL, RegisterPostData, Token, authenticate_user, create_access_token, get_current_user, get_password_hash
from backend.controller_instance import controller


router = APIRouter()
route_tags: List[str | Enum] = ['authentication']


@router.post('/' + TOKEN_URL, tags=route_tags)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if (not isinstance(user, User)) or (user is None):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    encode_data = {"sub": user.get_email()}
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data=encode_data, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post('/register', tags=route_tags)
async def register(
    form_data: Annotated[RegisterPostData, Body(examples=[
        {
            "type": "user",
            "name": "Bob",
            "email": "bob@example.com",
            "password": "password"
        },
        {
            "type": "teacher",
            "name": "Alice",
            "email": "alice@example.com",
            "password": "password"
        }
    ])]
) -> Token:
    hashed_password = get_password_hash(form_data.password)
    if (form_data.type == 'user'):
        user = User(form_data.name, form_data.email, hashed_password)
    elif (form_data.type == 'teacher'):
        user = Teacher(form_data.name, form_data.email, hashed_password)
    controller.add_user(user)
    
    if (not isinstance(user, User)) or (user is None):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    encode_data = {"sub": user.get_email()}
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data=encode_data, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/account", tags=route_tags)
async def get_my_account_info(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
