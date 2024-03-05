from typing import List, Union
from fastapi import APIRouter, Body
from pydantic import UUID4

from backend.definitions.course import Course, CourseCategory
from backend.definitions.user import User, Teacher
from backend.definitions.controller import Controller
from backend.controller_instance import controller
import random

from argon2 import PasswordHasher
password_hasher = PasswordHasher()

router = APIRouter()

category_programming = CourseCategory('Programming')
OOP = Course('OOP', 'Easy', 499, 'Thana')
C = Course('C', 'Easy', 199, 'Thanunchai')
category_programming.add_course(OOP)
category_programming.add_course(C)
controller.add_category(category_programming)

category_math = CourseCategory('Math')
Cal = Course('Cal', 'Easy', 399, 'Sakchai')
Discrete = Course('Discrete', 'Meduim', 199, 'Thanunchai')
category_math.add_course(Cal)
category_math.add_course(Discrete)
controller.add_category(category_math)

category_physics = CourseCategory('Physics')
Circuit = Course('Circuit', 'Easy', 299, 'Sorapong')
category_physics.add_course(Circuit)
controller.add_category(category_physics)

user_A = User('A', 'A@example.com', password_hasher.hash("password"))
controller.add_user(user_A)

user_B = User('B', 'B@example.com', password_hasher.hash("password"))
controller.add_user(user_B)

user_C = User('C', 'C@example.com',  password_hasher.hash("password"))
controller.add_user(user_C)

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


