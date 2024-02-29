from datetime import timedelta
from typing import Annotated
from fastapi import Depends, APIRouter
from backend.lib.authentication import User, get_current_user

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from backend.config import ACCESS_TOKEN_EXPIRE_MINUTES
from backend.lib.authentication import TOKEN_URL, User, Token, UserInDB, authenticate_user, create_access_token, get_current_active_user, fake_users_db


router = APIRouter()


@router.post('/' + TOKEN_URL)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if (not isinstance(user, UserInDB)) or (user is bool):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    encode_data = {"sub": user.username}
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data=encode_data, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]
