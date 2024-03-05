from typing import List, Union
from fastapi import APIRouter, Body
from pydantic import UUID4

from backend.definitions.course import Course, CourseCatergory
from backend.definitions.user import User, Teacher
from backend.definitions.controller import Controller
from backend.controller_instance import controller
import random

router = APIRouter()

category_programming = CourseCatergory('Programming')
OOP = Course('OOP', 'Easy', 499)
C = Course('C', 'Easy', 199)
category_programming.add_course(OOP)
category_programming.add_course(C)
controller.add_category(category_programming)

category_math = CourseCatergory('Math')
Cal = Course('Cal', 'Easy', 399)
Discrete = Course('Discrete', 'Meduim', 199)
category_math.add_course(Cal)
category_math.add_course(Discrete)
controller.add_category(category_math)

category_physics = CourseCatergory('Physics')
Circuit = Course('Circuit', 'Easy', 299)
category_physics.add_course(Circuit)
controller.add_category(category_physics)

@router.get("/course/homepage/random_course")
def random_course():
    all_courses = controller.get_all_courses()
    return random.sample(all_courses, 3)

@router.get("/course/homepage/suggestion")

def suggest_course():
    reviewed_course = []
    for course in controller.get_all_courses():
        if course.get_reviews():
            reviewed_course.append(course)

    # courses_sorted = sorted(suggest_course, key=lambda x: x["_Course__reviews"][0]["_CourseReview__star"], reverse=True)

    return reviewed_course
            
    # return suggest_course

# print(course[0]["_Course__reviews"][0]["_CourseReview__star"])



