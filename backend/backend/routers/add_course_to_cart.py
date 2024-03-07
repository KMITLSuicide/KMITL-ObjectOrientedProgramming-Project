from typing import List, Union
from fastapi import APIRouter, Body
from pydantic import UUID4, BaseModel

from backend.definitions.course import Course
from backend.definitions.user import User, Teacher
from backend.definitions.controller import Controller
from backend.controller_instance import controller

router = APIRouter()

class AddCourse(BaseModel):
    id: str
    name: str

# @router.get("/user/{user_name}")
# def get_user(user_name: str):
#     return controller.get_users_by_name(user_name)

# @router.get("/course/{course_name}")
# def get_course(course_name: str):
#     return controller.search_course_by_name(course_name)

    
@router.post('/user/{user_id}/cart/')
def add_course_to_cart(user_id: UUID4,
                       course_id_query: UUID4):
    obj_user = controller.get_user_by_id(user_id)

    if isinstance(obj_user, User):
        obj_cart = obj_user.get_cart()

    obj_course = controller.search_course_by_id(course_id_query)

    obj_cart.add_course(obj_course)

    return obj_cart

# @router.get("/course", tags=route_tags)
# def get_all_course():
#     return_data: List[GetAllCourse] = []
#     all_course = controller.get_all_courses()
#     for course in all_course:
#         return_data.append(
#             GetAllCourse(
#                 id=str(course.get_id()),
#                 name=course.get_name()
#             ))
#     return return_data

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
    obj_user = controller.get_user_by_id(user_id)

    if isinstance(obj_user, User):
        obj_cart = obj_user.get_cart()

    return obj_cart
