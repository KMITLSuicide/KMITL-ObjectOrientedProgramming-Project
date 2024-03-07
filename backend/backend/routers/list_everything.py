from typing import List, Union
from fastapi import APIRouter, Body
from pydantic import UUID4

from backend.definitions.course import Course
from backend.definitions.user import User, Teacher
from backend.definitions.controller import Controller
from backend.controller_instance import controller
import random

router = APIRouter()

@router.get("/course/all_course/")
def get_all_course_list():
    all_courses = controller.get_all_courses()
    return all_courses

@router.get("/teacher/all_teacher")
def get_all_teacher_list():
    return controller.get_all_teacher()

@router.get("/user/all_user")
def get_all_user():
    return controller.get_all_user()


