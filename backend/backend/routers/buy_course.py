from typing import List, Union
from fastapi import APIRouter, Body
from pydantic import UUID4

from backend.definitions.course import Course
from backend.definitions.user import User, Teacher
from backend.definitions.controller import Controller
from backend.definitions.progress import Progress
from backend.controller_instance import controller

router = APIRouter()

@router.get("/buy_course/{user_id}/{status}/{course_id}")
def buy_course(user_id:UUID4, status:bool, course_id:UUID4):
    
    user = controller.get_user_by_id(user_id)

    if not isinstance(user, User):
        return "Error: User not instance"
    
    if status != True:
        return "Error: Status not True"
    
    course = controller.search_course_by_id(course_id)
    
    if course == None:
        return "Error course is None"
    
    for progress_in_user in user.view_my_learning():
        if course == progress_in_user.get_course:
            return f"Error you already have {course.get_name} course"
    
    new_progress = Progress(course)
    
    user.add_progress(new_progress)    
    
    discount = 0
    
    controller.create_order(user, course, discount, status)
    
    return f"add {course.get_name()} course succesful",user.get_orders , user.view_my_learning()