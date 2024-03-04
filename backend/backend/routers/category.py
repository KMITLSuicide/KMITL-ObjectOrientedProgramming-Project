from enum import Enum
from typing import List
import uuid
from fastapi import APIRouter

from backend.controller_instance import controller


router = APIRouter()
route_tags: List[str | Enum] = ["category"]


@router.get("/category", tags=route_tags)
def get_all_categories():
    return controller.get_all_categories()


@router.get("/category/{category_id}", tags=route_tags)
def get_category_by_id(category_id: str):
    category = controller.search_category_by_id(uuid.UUID(category_id))
    return category
