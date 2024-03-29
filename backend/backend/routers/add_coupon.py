# from enum import Enum
# from uuid import UUID
# from typing import List, Annotated, Literal, Annotated
# from fastapi import APIRouter, Depends, Response, status, Body, Depends
# from pydantic import BaseModel
# from backend.controller_instance import controller
# from backend.definitions.progress import Progress
# from backend.definitions.course import Course
# from backend.definitions.user import User,Teacher
# from backend.lib.authentication import get_current_user
# router = APIRouter()

# route_tags: List[str | Enum] = ["Coupon"]

# class CouponData(BaseModel):
#     coupon_id: str
#     discount: int

# class CouponCourseData(BaseModel):
#     type: str
#     coupon_id: str
#     discount: int
#     teacher_name: str
#     course_name: str
#     course_id: str

# class CouponTeacherData(BaseModel):
#     type: str
#     coupon_id: str
#     discount: int
#     teacher_name: str

# @router.get("/coupon", tags=["Debug Purposes"])
# def get_all_coupon():
#     return_data = []
#     for coupon in controller.get_all_coupons():
#         if isinstance(coupon, CouponTeacher):
#             return_data.append(
#                 CouponTeacherData(
#                     type="Teacher Coupon",
#                     coupon_id=str(coupon.get_id()),
#                     discount=coupon.get_discount(),
#                     teacher_name=str(coupon.get_teacher().get_name())
#                 )
#             )
#         elif isinstance(coupon, CouponCourse):
#             return_data.append(
#                 CouponCourseData(
#                     type="Course Coupon",
#                     coupon_id=str(coupon.get_id()),
#                     discount=coupon.get_discount(),
#                     teacher_name=str(coupon.get_teacher().get_name()),
#                     course_name=str(coupon.get_course().get_name()),
#                     course_id=str(coupon.get_course().get_id())
#                 )
#             )
#         else:
#             return_data.append(
#                 "Error Warning"
#             )
#     return return_data


# @router.post("/teacher/coupon/course/{course_id}", tags=route_tags)
# def add_coupon_course(
#     current_user: Annotated[Teacher, Depends(get_current_user)],
#     course_id: UUID,
#     add_coupon_data: Annotated[CouponData, Body(
#         examples=[
#             {
#                 "coupon_id": "course",
#                   "discount": 999
#                   }
#             ]),],):
#     course = controller.search_course_by_id(course_id)
#     if not isinstance(course, Course):
#         return "Error: Course is not instance"
#     controller.add_coupon_course(add_coupon_data.coupon_id, add_coupon_data.discount, course, current_user)
#     return_data = []
#     for coupon in controller.get_all_coupons():
#         if isinstance(coupon, CouponTeacher):
#             return_data.append(
#                 CouponTeacherData(
#                     type="Teacher Coupon",
#                     coupon_id=str(coupon.get_id()),
#                     discount=coupon.get_discount(),
#                     teacher_name=str(coupon.get_teacher().get_name())
#                 )
#             )
#         elif isinstance(coupon, CouponCourse):
#             return_data.append(
#                 CouponCourseData(
#                     type="Course Coupon",
#                     coupon_id=str(coupon.get_id()),
#                     discount=coupon.get_discount(),
#                     teacher_name=str(coupon.get_teacher().get_name()),
#                     course_name=str(coupon.get_course().get_name()),
#                     course_id=str(coupon.get_course().get_id())
#                 )
#             )
#         else:
#             return_data.append(
#                 "Error Warning"
#             )
#     return return_data


# @router.post("/teacher/coupon/teacher", tags=route_tags)
# def add_coupon_teacher(
#     current_user: Annotated[Teacher, Depends(get_current_user)],
#     add_coupon_data: Annotated[CouponData, Body(
#         examples=[
#             {
#                 "coupon_id": "teacher",
#                 "discount": 999
#                 }
#             ]),],):
#     controller.add_coupon_teacher(add_coupon_data.coupon_id, add_coupon_data.discount, current_user)
#     return_data = []
#     for coupon in controller.get_all_coupons():
#         if isinstance(coupon, CouponTeacher):
#             return_data.append(
#                 CouponTeacherData(
#                     type="Teacher Coupon",
#                     coupon_id=str(coupon.get_id()),
#                     discount=coupon.get_discount(),
#                     teacher_name=str(coupon.get_teacher().get_name())
#                 )
#             )
#         elif isinstance(coupon, CouponCourse):
#             return_data.append(
#                 CouponCourseData(
#                     type="Course Coupon",
#                     coupon_id=str(coupon.get_id()),
#                     discount=coupon.get_discount(),
#                     teacher_name=str(coupon.get_teacher().get_name()),
#                     course_name=str(coupon.get_course().get_name()),
#                     course_id=str(coupon.get_course().get_id())
#                 )
#             )
#         else:
#             return_data.append(
#                 "Error Warning"
#             )
#     return return_data