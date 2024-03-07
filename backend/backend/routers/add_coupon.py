# from fastapi import APIRouter, Body, Depends
# from pydantic import UUID4
# from enum import Enum
# from typing import List, Annotated

# from backend.definitions.course import Course
# from backend.definitions.user import User, Teacher
# from backend.definitions.controller import Controller
# from backend.definitions.progress import Progress
# from backend.controller_instance import controller
# from backend.lib.authentication import get_current_user

# router = APIRouter()
# route_tags: List[str | Enum] = ["coupon"]

# @router.post("/teacher/add_coupon_course/{coupon_id}/{discount}/{course_id}", tags=route_tags)
# def add_coupon_course(current_teacher: Annotated[Teacher, Depends(get_current_user)],
#                       coupon_id: int,
#                       coupon_data:
#                         Annotated[CouponData, Body(
#                           example=[
#                             {
#                               "discount": 1000,
#                               "course_id":1234,
#                             }
#                           ]
#                         )])

# @router.post("/add_coupon_course/{coupon_id}/{discount}/{course_id}", tags=route_tags)
# def add_coupon_course(coupon_id, discount:int, course_id:UUID4):
#   course = controller.search_course_by_id(course_id)
#   if course == None:
#     return "Error: Course is none"
#   controller.add_coupon_course(coupon_id, discount, course)
#   return controller.get_all_coupons()

# @router.post("/add_coupon_teacher/{coupon_id}/{discount}/{teacher_id}", tags=route_tags)
# def add_coupon_teacher(coupon_id, discount:int, teacher_id:UUID4):
#   teacher = controller.get_teacher_by_id(teacher_id)
#   if not isinstance(teacher, Teacher):
#     return "Error: Teacher is none"
#   controller.add_coupon_teacher(coupon_id, discount, teacher)
#   return controller.get_all_coupons()