from typing import List, Union
from fastapi import APIRouter, Body
from pydantic import UUID4, BaseModel

from backend.definitions.course import Course
from backend.definitions.user import User, Teacher
from backend.definitions.controller import Controller
from backend.controller_instance import controller
from backend.definitions.api_data_model import CourseCardData
import random

router = APIRouter()

@router.get("/course/homepage/random_course")
def random_course():
    return_data: List[CourseCardData] = []
    all_course = controller.get_all_courses()
    for course in all_course:
        return_data.append(
            CourseCardData(
                id = str(course.get_id()),
                name = course.get_name(),
                description = course.get_description(),
                price = course.get_price(),
                rating = 0,
                banner_image = course.get_banner_image_url()
        ))
    random_course = random.sample(return_data, 3)
    return random_course


@router.get("/course/homepage/suggestion")
def suggest_course():
    return_data: List[CourseCardData] = []
    all_course = controller.get_all_courses()
    for course in all_course:
        if course.get_reviews():
            return_data.append(
                CourseCardData(
                    id = str(course.get_id()),
                    name = course.get_name(),
                    description = course.get_description(),
                    price = course.get_price(),
                    rating = 0,
                    banner_image = course.get_banner_image_url()
                ))
    return return_data
