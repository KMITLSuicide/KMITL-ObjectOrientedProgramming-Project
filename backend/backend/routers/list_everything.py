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

@router.get("/course/all_course/", tags = route_tags)
def get_all_course_list():
    all_courses = controller.get_all_courses()
    return all_courses

@router.get("/teacher/all_teacher", tags = route_tags)
def get_all_teacher_list():
    return controller.get_all_teacher()


#for debug only
@router.get("/user", tags=route_tags)
def get_all_user():
    return controller.get_all_user()



