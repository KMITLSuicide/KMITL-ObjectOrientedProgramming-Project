from typing import List, Union
from fastapi import APIRouter, Body

from backend.definitions.course import Course
from backend.definitions.user import User, Teacher
from backend.definitions.controller import Controller
from backend.controller_instance import controller

router = APIRouter()

@router.get("/")
def hello():
    return "hello world"

@router.get("/search/course/{course_name}")
def get_search_course(course_name: str):
    return controller.search_course_by_name(course_name)

@router.get("/search/category/{category_name}")
def get_search_category(category_name: str):
    return controller.search_category_by_name(category_name)

@router.get("/search/teacher/{teacher_name}")
def get_search_teacher(teacher_name: str):
    return controller.search_teacher_by_name(teacher_name)

