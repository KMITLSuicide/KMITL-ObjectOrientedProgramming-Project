from enum import Enum
from uuid import UUID
from typing import List, Annotated, Literal, Annotated
from fastapi import APIRouter, Depends, Response, status, Body, Depends
from pydantic import BaseModel
from backend.controller_instance import controller
from backend.definitions.progress import Progress
from backend.definitions.course import Course
from backend.definitions.user import User,Teacher
from backend.lib.authentication import get_current_user

router = APIRouter()

route_tags: List[str | Enum] = ["Cart"]
    
@router.post('/user/add_course_to_cart',tags= route_tags)
def add_course_to_cart(current_user: Annotated[User, Depends(get_current_user)],
                       course_id_query: UUID):

    obj_course = controller.search_course_by_id(course_id_query)
    obj_cart = current_user.get_cart()
    obj_cart.add_course(obj_course)

    return obj_cart

@router.delete('/user/remove_course_to_cart',tags= route_tags)
def remove_course_to_cart(current_user: Annotated[User, Depends(get_current_user)], course_id_query: UUID):

    obj_course = controller.search_course_by_id(course_id_query)
    obj_cart = current_user.get_cart()
    obj_cart.remove_course(obj_course)

    return obj_cart

@router.get('/user/get_course_in_cart/',tags= route_tags)
def get_course_in_cart(current_user: Annotated[User, Depends(get_current_user)], course_id_query: UUID):
    return current_user.get_cart()
