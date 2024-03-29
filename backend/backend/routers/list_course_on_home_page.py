from typing import List
from fastapi import APIRouter, Body, HTTPException
from pydantic import UUID4, BaseModel
from uuid import UUID
from enum import Enum
from backend.definitions.course import Course
from backend.definitions.user import User, Teacher
from backend.definitions.controller import Controller
from backend.controller_instance import controller
from backend.definitions.api_data_model import CourseCardData
import random

router = APIRouter()

route_tags: List[str | Enum] = ["HomePage"]

class ShowCourse(BaseModel):
    id: str
    name: str
    description: str
    price: float
    rating: float
    banner_image: str
    star: float

@router.get("/course/homepage/random_course", tags= route_tags)
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
                rating = course.get_average_rating(),
                banner_image = course.get_banner_image_url()
        ))
    random_course = random.sample(return_data, 3)
    return random_course


@router.get("/course/homepage/random_reviewed_course", tags= route_tags)
def random_reviewed_course():
    random_amount = 3
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
                    rating = course.get_average_rating(),
                    banner_image = course.get_banner_image_url()
                ))
    if not return_data:
        return_data = []
    random_reviewed_course = random.sample(return_data, random_amount)
    return random_reviewed_course

@router.get("/course/homepage/suggestion", tags=route_tags)
def suggest_course():
    return_data: list[CourseCardData] = []
    
    # Call the sort_course_by_rating method
    sorted_courses = controller.sort_course_by_rating()
    if not sorted_courses:
        return []
    for course in sorted_courses:
        if not isinstance(course, Course):
            return 'Error'
        if course.get_reviews():
            return_data.append(
                CourseCardData(
                    id=str(course.get_id()),
                    name=course.get_name(),
                    description=course.get_description(),
                    price=course.get_price(),
                    rating=course.get_average_rating(),
                    banner_image=course.get_banner_image_url()
                ))
            
            # Limit the number of suggested courses to 3
            if len(return_data) == 3:
                break
    
    return return_data

