from typing import List
from enum import Enum
from uuid import UUID
from fastapi import APIRouter, HTTPException,status

from backend.controller_instance import controller
from backend.definitions.api_data_model import CourseCardData, CourseCardDataWithLabel
from backend.definitions.user import Teacher


router = APIRouter()

route_tags: List[str | Enum] = ["Teacher"]


@router.get("/teacher/{teacher_id}/course", tags=["Course"])
def get_courses_for_teacher(teacher_id: UUID):
    teacher = controller.get_teacher_by_id(teacher_id)
    if not isinstance(teacher, Teacher):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Teacher id not found",
        ) 
    search_results: CourseCardDataWithLabel = CourseCardDataWithLabel(
        id=str(teacher.get_id()), label=teacher.get_name(), cards=[]
    )
    for course in teacher.get_my_teachings():
        search_results.cards.append(
            CourseCardData(
                id=str(course.get_id()),
                name=course.get_name(),
                description=course.get_description(),
                price=course.get_price(),
                rating=course.get_average_rating(),
                banner_image=course.get_banner_image_url(),
            )
        )
    return search_results
