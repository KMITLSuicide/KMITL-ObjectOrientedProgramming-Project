from typing import List, Union
from fastapi import APIRouter, Body
from pydantic import UUID4
from enum import Enum
from backend.definitions.course import Course
from backend.definitions.user import User, Teacher
from backend.definitions.controller import Controller
from backend.controller_instance import controller
import random

router = APIRouter()

route_tags: List[str | Enum] = ["Debug Purposes"]


@router.get("/teacher/all_teacher", tags = route_tags)
def get_all_teacher_list():
    teacher_list = controller.get_all_teacher()
    return teacher_list


#for debug only
@router.get("/user", tags=route_tags)
def get_all_user():
    return controller.get_all_user()



