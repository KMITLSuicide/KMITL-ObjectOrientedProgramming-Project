from enum import Enum
from uuid import UUID
from typing import List, Annotated, Literal, Annotated
from fastapi import APIRouter, Depends, Response, status, Body, Depends
from pydantic import BaseModel
from backend.controller_instance import controller
from backend.definitions.progress import Progress
from backend.definitions.course import Course
from backend.definitions.user import User,Teacher
from backend.lib.authentication import get_current_user


router = APIRouter()
route_tags: List[str | Enum] = ["View Video"]


@router.get("/user/view_my_learning", tags=route_tags)
def view_my_learning(current_user : Annotated[User,Depends(get_current_user)]):
    my_progresses = current_user.view_my_learning()
    return my_progresses

@router.get("/user/view_video/{video_name}", tags= route_tags)
async def view_video(current_user: Annotated[User, Depends(get_current_user)], video_name: str):
    video = current_user.view_video_by_name(video_name)
    return {"video": video}

@router.get("/user/study_latest_video", tags=route_tags)
async def study_latest_course(current_user: Annotated[User, Depends(get_current_user)]):
    latest_video = current_user.get_latest_video()
    return latest_video

@router.get("/user/search_course_by_id/{course_id}", tags=["Course"])
def get_course_by_id(current_user: Annotated[User, Depends(get_current_user)], course_id: UUID):
    course = current_user.search_course_by_id(course_id)
    return course

@router.get("/user/get_my_teaching", tags=["My Teaching"])
def get_my_teaching(current_user: Annotated[User, Depends(get_current_user)]):
    if not isinstance(current_user, Teacher):
        return "Error, You r not teacher"
    return current_user.get_my_teachings()


class AccountInfo(BaseException):
    type: Literal['user', 'teacher']
    id: str
    name: str
    email: str

@router.get("/account", tags=["User"])
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
