from enum import Enum
from typing import List, Annotated, Literal
from fastapi import APIRouter, Depends

from backend.controller_instance import controller
from backend.definitions.user import User, Teacher
from backend.lib.authentication import get_current_user


router = APIRouter()
route_tags: List[str | Enum] = ["user"]


@router.get("/user", tags=route_tags)
def get_all_user():
    return controller.get_all_user()


@router.get("/teacher", tags=route_tags)
def get_all_teacher():
    return controller.get_all_teacher()


class AccountInfo(BaseException):
    type: Literal['user', 'teacher']
    id: str
    name: str
    email: str

@router.get("/account", tags=route_tags)
async def get_my_account_info(current_user: Annotated[User, Depends(get_current_user)]):
    user_type = 'user'
    if isinstance(current_user, Teacher):
        user_type = 'teacher'

    return {
        "type": user_type,
        "id": str(current_user.get_id()),
        "name": current_user.get_name(),
        "email": current_user.get_email(),
        }
