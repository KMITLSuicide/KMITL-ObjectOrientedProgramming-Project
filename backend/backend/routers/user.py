from enum import Enum
from uuid import UUID
from typing import List, Annotated
from fastapi import APIRouter, Response, status, Body, Depends
from pydantic import BaseModel
from backend.controller_instance import controller
from backend.definitions.progress import Progress
from backend.definitions.course import Course
from backend.definitions.user import User
from backend.lib.authentication import get_current_user


router = APIRouter()
route_tags: List[str | Enum] = ["user"]


@router.get("/user", tags=route_tags)
def get_all_user():
    return controller.get_all_user()


@router.get("/teacher", tags=route_tags)
def get_all_teacher():
    return controller.get_all_teacher()
@router.get("/user/view_my_learning", tags=route_tags)

def view_my_learning(current_user : Annotated[User,Depends(get_current_user)]):
    my_progresses = current_user.view_my_learning()
    return my_progresses