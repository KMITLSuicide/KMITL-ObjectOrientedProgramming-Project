from typing import List, Union
from fastapi import APIRouter, Body
from pydantic import UUID4, BaseModel

from backend.definitions.course import Course
from backend.definitions.user import User, Teacher
from backend.definitions.controller import Controller
from backend.controller_instance import controller
import random

router = APIRouter()

class GetRandomCourse(BaseModel):
    id: str
    name: str

@router.get("/course/homepage/random_course")
def random_course():
    return_data: List[GetRandomCourse] = []
    all_course = controller.get_all_courses()
    for course in all_course:
        return_data.append(
            GetRandomCourse(
                id = str(course.get_id()),
                name = course.get_name()
            )
        )
    # random_course = random.sample(all_course, 3)
    return all_course

# @router.get("/user", tags=route_tags)
# def get_all_user():
#     return_data: list[GetAllUser] = []
#     all_users = controller.get_all_user()
#     for user in all_users:
#         return_data.append(
#             GetAllUser(
#                 id=str(user.get_id()),
#                 name=user.get_name()
#             ))
#     return return_data


# @router.get("/course/homepage/suggestion")
# def suggest_course():
#     reviewed_course = []
#     for course in controller.get_all_courses():
#         if course.get_reviews():
#             reviewed_course.append(course)

#     return reviewed_course
            
