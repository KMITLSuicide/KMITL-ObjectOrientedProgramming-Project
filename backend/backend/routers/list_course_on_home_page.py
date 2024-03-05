from typing import List, Union
from fastapi import APIRouter, Body
from pydantic import UUID4

from backend.definitions.course import Course
from backend.definitions.user import User, Teacher
from backend.definitions.controller import Controller
from backend.controller_instance import controller
import random

router = APIRouter()

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
