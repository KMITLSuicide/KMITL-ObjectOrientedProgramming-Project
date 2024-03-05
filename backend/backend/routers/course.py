from enum import Enum
from typing import List
import uuid
from fastapi import APIRouter

from backend.controller_instance import controller


router = APIRouter()
route_tags: List[str | Enum] = ["course"]


@router.get("/course", tags=route_tags)
def get_all_course():
    return controller.get_all_courses()


@router.get("/course/{course_id}", tags=route_tags)
def get_course_by_id(course_id: str):
    course = controller.search_course_by_id(uuid.UUID(course_id))
    return course
