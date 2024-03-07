from typing import List
from enum import Enum
from fastapi import APIRouter
from pydantic import BaseModel

from backend.controller_instance import controller


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
    search_results: List[SearchResults] = []
    courses = controller.search_course_by_name(course_name)
    for course in courses:
        search_results.append(SearchResults(name=course.get_name(), id=str(course.get_id())))
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
