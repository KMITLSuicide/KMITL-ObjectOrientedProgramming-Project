from typing import List
from enum import Enum
from fastapi import APIRouter
from pydantic import BaseModel

from backend.controller_instance import controller
from backend.definitions.api_data_model import CourseCardData
from backend.definitions.course import Course
from backend.definitions.user import Teacher
from uuid import UUID
router = APIRouter()
route_tags: List[str | Enum] = ["Search"]


class SearchResults(BaseModel):
    name: str
    id: str

@router.get("/", tags = ["Debug Purposes"])
def hello():
    return "hello world"

@router.get("/search/course/{course_name}", tags=route_tags)
def get_search_course(course_name: str):
    search_results: List[CourseCardData] = []
    courses = controller.search_course_by_name(course_name)
    for course in courses:
        search_results.append(
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


@router.get("/search/category/{category_name}", tags=route_tags)
def get_search_category(category_name: str):
    search_results: List[SearchResults] = []
    categories = controller.search_category_by_name(category_name)
    for category in categories:
        search_results.append(SearchResults(name=category.get_name(), id=str(category.get_id())))
    return search_results

@router.get("/search/teacher/{teacher_name}", tags=route_tags)
def get_search_teacher(teacher_name: str):
    search_results: List[SearchResults] = []
    teachers = controller.search_teacher_by_name(teacher_name)
    for teacher in teachers:
        search_results.append(SearchResults(name=teacher.get_name(), id=str(teacher.get_id())))
    return search_results



@router.get("/get_courses_for_teacher/{teacher_id}", tags=["Course"])
def get_courses_for_teacher(teacher_id: UUID):
    search_results: List[CourseCardData] = []
    teacher = controller.get_teacher_by_id(teacher_id)
    if not isinstance(teacher, Teacher):
        return "Error teacher is not instance of Teacher"
    for course in teacher.get_my_teachings():
        search_results.append(            
            CourseCardData(
                id=str(course.get_id()),
                name=course.get_name(),
                description=course.get_description(),
                price=course.get_price(),
                rating= course.get_average_rating(),
                banner_image=course.get_banner_image_url(),
            )
        )
    return search_results