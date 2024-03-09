from enum import Enum
from uuid import UUID
from typing import List, Annotated, Literal, Annotated
from fastapi import APIRouter, Depends, Response, status, Body, Depends, HTTPException
from pydantic import BaseModel
from backend.controller_instance import controller
from backend.definitions.progress import Progress
from backend.definitions.course import Course
from backend.definitions.user import User,Teacher
from backend.lib.authentication import get_current_user
from backend.definitions.api_data_model import CourseCardData

router = APIRouter()

route_tags: List[str | Enum] = ["Cart"]
    
@router.post('/user/cart',tags= route_tags)
def add_course_to_cart(current_user: Annotated[User, Depends(get_current_user)],
                       course_id: str):
    return_cart: list[CourseCardData] = []

    obj_course = controller.search_course_by_id(UUID(course_id))

    if isinstance(current_user, User):
        obj_cart = current_user.get_cart()

    if obj_course in obj_cart.get_courses():
        raise HTTPException(status_code=400)#Fail
        
    obj_cart.add_course(obj_course)

    for course in obj_cart.get_courses():
        return_cart.append(
            CourseCardData(
                id = str(course.get_id()),
                name = course.get_name(),
                description = course.get_description(),
                price = course.get_price(),
                rating = course.get_average_rating(),
                banner_image = course.get_banner_image_url()
        ))
    return return_cart

@router.delete('/user/cart',tags= route_tags)
def remove_course_to_cart(current_user: Annotated[User, Depends(get_current_user)], course_id: UUID):

    obj_course = controller.search_course_by_id(course_id)
    obj_cart = current_user.get_cart()
    if obj_course not in obj_cart.get_courses():
        raise HTTPException(status_code=400)#Fail
    obj_cart.remove_course(obj_course)

    return HTTPException(status_code=200)#Succeed

@router.get('/user/cart',tags= route_tags)
def get_course_in_cart(current_user: Annotated[User, Depends(get_current_user)]):
    return_cart: list[CourseCardData] = []

    if isinstance(current_user, User):
        obj_cart = current_user.get_cart()

    for course in obj_cart.get_courses():
        return_cart.append(
            CourseCardData(
                id = str(course.get_id()),
                name = course.get_name(),
                description = course.get_description(),
                price = course.get_price(),
                rating = course.get_average_rating(),
                banner_image = course.get_banner_image_url()
        ))

    return return_cart
