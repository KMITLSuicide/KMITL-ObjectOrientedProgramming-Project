from typing import List, Union
from fastapi import APIRouter, Body

from backend.definitions.course import Course, CourseCategory
from backend.definitions.user import User, Teacher
from backend.definitions.controller import Controller
from backend.controller_instance import controller

from argon2 import PasswordHasher
password_hasher = PasswordHasher()

router = APIRouter()

category_programming = CourseCategory('Programming')
programming_course = Course('OOP', 'Easy', 499, 'Thana')
category_programming.add_course(programming_course)
controller.add_category(category_programming)

category_math = CourseCategory('Math')
math_course = Course('Calculus', 'Medium', 399, 'Sakchai')
category_math.add_course(math_course)
controller.add_category(category_math)

category_physics = CourseCategory('Physics')
physics_course = Course('Circuit', 'Hard', 299, 'Surapong')
category_physics.add_course(physics_course)
controller.add_category(category_physics)

controller.add_teacher(Teacher('Thana', 'Thana@example.com', password_hasher.hash("password")))
controller.add_teacher(Teacher('Sakchai', 'Sakchai@example.com', password_hasher.hash("password")))
controller.add_teacher(Teacher('Sorapong', 'Sorapong@example.com', password_hasher.hash("password")))

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

