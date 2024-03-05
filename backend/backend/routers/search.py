from typing import List, Union
from fastapi import APIRouter, Body

from backend.definitions.course import Course, CourseCatergory
from backend.definitions.user import User, Teacher
from backend.definitions.controller import Controller
from backend.controller_instance import controller


router = APIRouter()

category_programming = CourseCatergory('Programming')
programming_course = Course('OOP', 'Easy', 499)
category_programming.add_course(programming_course)
controller.add_category(category_programming)

category_math = CourseCatergory('Math')
math_course = Course('Calculus', 'Medium', 399)
category_math.add_course(math_course)
controller.add_category(category_math)

category_physics = CourseCatergory('Physics')
physics_course = Course('Circuit', 'Hard', 299)
category_physics.add_course(physics_course)
controller.add_category(category_physics)

controller.add_teacher(Teacher('Thana'))
controller.add_teacher(Teacher('Sakchai'))
controller.add_teacher(Teacher('Sorapong'))

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

