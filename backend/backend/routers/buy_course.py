from enum import Enum
from uuid import UUID
from typing import List, Annotated, Literal, Annotated
from fastapi import APIRouter, Depends, Response, status, Body, Depends
from pydantic import BaseModel
from backend.controller_instance import controller
from backend.definitions.progress import Progress
from backend.definitions.course import Course
from backend.definitions.user import User,Teacher
from backend.lib.authentication import get_current_user
router = APIRouter()

route_tags: List[str | Enum] = ["Course"]

class BuyCourseData(BaseModel):
    status: bool
    coupon_id: UUID | None



@router.post("/user/buy_course/{course_id}", tags=route_tags)
def buy_course(
    current_user: Annotated[User, Depends(get_current_user)],
    course_id: UUID,
    buy_course_data: Annotated[BuyCourseData, Body(            
            examples=[
                {
                    "status": True,
                    "coupon_id": "adfasbasdfaskldfjasdfka",
                }
            ]),],
):
    result = controller.buy_course(
        current_user, buy_course_data.status, course_id, buy_course_data.coupon_id
    )
    return result