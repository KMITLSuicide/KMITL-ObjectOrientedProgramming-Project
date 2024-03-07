from typing import List
from enum import Enum
from fastapi import APIRouter
from pydantic import BaseModel

from backend.controller_instance import controller
from backend.backend.definitions.api_data_model import CourseCardData,CategoryInfo
from backend.backend.definitions.course import Course

router = APIRouter()
route_tags: List[str | Enum] = ["search"]


class SearchResults(BaseModel):
    name: str
    id: str

@router.get("/")
def hello():
    return "hello world"

@router.get("/search/course/{course_name}", tags=route_tags)
def get_search_course(course_name: str):
    search_results: List[CourseCardData] = []
    courses = controller.search_course_by_name(course_name)
    for course in courses:
        search_results.append
        (            
            CourseCardData
            (
                id=str(course.get_id()),
                name=course.get_name(),
                description=course.get_description(),
                price=course.get_price(),
                rating=0,
                banner_image=course.get_banner_image_url(),
            )
        )
    return search_results


@router.get("/search/category/{category_name}", tags=route_tags)
def get_search_category(category_name: str):
    search_results: List[CategoryInfo] = []
    categories = controller.search_category_by_name(category_name)
    for category in categories:
        course_card_data_list : List[CourseCardData] = []
        for course in category.get_courses():
            if not isinstance(course, Course):
                return "Error course in category list is not instance of Course"
            course_card_data_list.append
            (
                CourseCardData(
                    id=str(course.get_id()),
                    name=course.get_name(),
                    description=course.get_description(),
                    price=course.get_price(),
                    rating=0,
                    banner_image=course.get_banner_image_url(),
                )
            )
        search_results.append
        (
            CategoryInfo
            (
                id= str(category.get_id()), name = category.get_name(),  courses = course_card_data_list
                
            )
        )
    return search_results

@router.get("/search/teacher/{teacher_name}", tags=route_tags)
def get_search_teacher(teacher_name: str):
    search_results: List[SearchResults] = []
    teachers = controller.search_teacher_by_name(teacher_name)
    for teacher in teachers:
        search_results.append(SearchResults(name=teacher.get_name(), id=str(teacher.get_id())))
    return search_results
