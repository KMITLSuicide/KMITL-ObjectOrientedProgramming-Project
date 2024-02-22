from typing import Annotated
from fastapi import Depends, APIRouter
from backend.lib.authentication import User, get_current_user


router = APIRouter()



@router.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user