import uuid
from fastapi import APIRouter

from backend.controller_instance import controller


router = APIRouter()


@router.get("/course")
def get_all_course():
    return controller.get_all_courses()

@router.get("/course/{course_id}")
def get_course_by_id(course_id: str):
    course = controller.search_course_by_id(uuid.UUID(course_id))
    return course
