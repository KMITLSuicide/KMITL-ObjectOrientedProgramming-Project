from typing import List, Union
from fastapi import APIRouter, Body
from pydantic import UUID4, BaseModel
from enum import Enum
from uuid import UUID

from backend.definitions.course import Course
from backend.definitions.user import User, Teacher
from backend.definitions.controller import Controller
from backend.controller_instance import controller
from backend.definitions.api_data_model import CourseCardData

router = APIRouter()
route_tags: List[str | Enum] = ["cart"]
    
@router.post('/user/{user_id}/cart/')
def add_course_to_cart(user_id: str,
                       course_id_query: str):
    return_cart: list[CourseCardData] = []

    obj_user = controller.get_user_by_id(UUID(user_id))

    obj_course = controller.search_course_by_id(UUID(course_id_query))

    if isinstance(obj_user, User):
        obj_cart = obj_user.get_cart()

    obj_cart.add_course(obj_course)

    # all_course = controller.get_all_courses()
    for course in obj_cart.get_courses():
        return_cart.append(
            CourseCardData(
                id = str(course.get_id()),
                name = course.get_name(),
                description = course.get_description(),
                price = course.get_price(),
                rating = 0,
                banner_image = course.get_banner_image_url()
        ))
    return return_cart

@router.delete('/user/{user_id}/cart/')
def remove_course_to_cart(user_id: UUID4, course_id_query: UUID4):
    obj_user = controller.get_user_by_id(user_id)

    if isinstance(obj_user, User):
        obj_cart = obj_user.get_cart()

    obj_course = controller.search_course_by_id(course_id_query)

    obj_cart.remove_course(obj_course)

    return obj_cart

@router.get('/user/{user_id}/cart/')
def get_course_in_cart(user_id: UUID4):
    return_cart: list[CourseCardData] = []
    obj_user = controller.get_user_by_id(user_id)

    if isinstance(obj_user, User):
        obj_cart = obj_user.get_cart()

    for course in obj_cart.get_courses():
        return_cart.append(
            CourseCardData(
                id = str(course.get_id()),
                name = course.get_name(),
                description = course.get_description(),
                price = course.get_price(),
                rating = 0,
                banner_image = course.get_banner_image_url()
        ))

    return return_cart

# def add_course_to_cart(user_id: str,
#                        course_id_query: str):
#     return_cart: list[CourseCardData] = []

#     obj_user = controller.get_user_by_id(UUID(user_id))

#     obj_course = controller.search_course_by_id(UUID(course_id_query))

#     if isinstance(obj_user, User):
#         obj_cart = obj_user.get_cart()

#     obj_cart.add_course(obj_course)

#     # all_course = controller.get_all_courses()
#     for course in obj_cart.get_courses():
#         return_cart.append(
#             CourseCardData(
#                 id = str(course.get_id()),
#                 name = course.get_name(),
#                 description = course.get_description(),
#                 price = course.get_price(),
#                 rating = 0,
#                 banner_image = course.get_banner_image_url()
#         ))
#     return return_cart