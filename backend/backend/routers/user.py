from enum import Enum
from typing import List
from fastapi import APIRouter

from backend.controller_instance import controller


router = APIRouter()
route_tags: List[str | Enum] = ["user"]


@router.get("/user", tags=route_tags)
def get_all_user():
    return controller.get_all_user()


@router.get("/teacher", tags=route_tags)
def get_all_teacher():
    return controller.get_all_teacher()
