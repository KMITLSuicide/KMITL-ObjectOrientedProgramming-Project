from enum import Enum
from typing import List
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.controller_instance import controller
from backend.definitions.course import CourseCategory
from backend.definitions.api_data_model import CourseCardData


router = APIRouter()
route_tags: List[str | Enum] = ["Category"]

class CategoryNames(BaseModel):
    id: str
    name: str


@router.get("/category", tags=["Debug Purposes"])
def get_all_categories():
    category_names: List[CategoryNames] = []
    for category in controller.get_all_categories():
        category_names.append(
            CategoryNames(id=str(category.get_id()), name=category.get_name())
        )
    return category_names


class CategoryInfo(BaseModel):
    id: str
    name: str
    courses: List[CourseCardData]


@router.get("/category/{category_id}", tags=route_tags)
def get_category_by_id(category_id: str):
    category = controller.search_category_by_id(uuid.UUID(category_id))
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    return_data = CategoryInfo(
        id=str(category.get_id()), name=category.get_name(), courses=[]
    )
    for course in category.get_courses():
        return_data.courses.append(
            CourseCardData(
                id=str(course.get_id()),
                name=course.get_name(),
                description=course.get_description(),
                price=course.get_price(),
                rating=course.get_average_rating(),
                banner_image=course.get_banner_image_url(),
            )
        )
    return return_data
