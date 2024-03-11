from enum import Enum
from uuid import UUID
from typing import List, Annotated, Literal, Annotated
from fastapi import APIRouter, Depends, Response, status, Body, Depends, HTTPException
from pydantic import BaseModel
from backend.controller_instance import controller
from backend.definitions.progress import Progress
from backend.definitions.course import Course
from backend.definitions.user import User,Teacher
from backend.lib.authentication import get_current_user
from backend.definitions.order import Payment
from backend.definitions.controller import Coupon
router = APIRouter()

route_tags: List[str | Enum] = ["Course"]

class BuyCourseData(BaseModel):
    status: bool
    # coupon_id: UUID | None
    coupon_id: str| None


class Bill(BaseModel):
    status:bool
    user_id:UUID
    course_id:UUID
    coupon_id:str
    price:int
    discount:int
    amout:int
    payment:str


@router.post("/user/buy/course/{course_id}", tags=route_tags)
def buy_course(
    current_user: Annotated[User, Depends(get_current_user)],
    course_id: UUID,
    buy_course_data: Annotated[BuyCourseData, Body(
            examples=[
                {
                    "status": True,
                    "coupon_id": "None",
                }
            ]),],
):
    result = controller.buy_course(
        current_user, buy_course_data.status, course_id, buy_course_data.coupon_id
    )
    return_data = []
    coupon = controller.search_coupon_by_id(buy_course_data.coupon_id)
    discounts = 0
    if isinstance(coupon, Coupon):
        discounts = coupon.get_discount()
        
    course = controller.search_course_by_id(course_id)
    if result == True and isinstance(course, Course):
        if course in current_user.get_my_progresses():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = "You alraeady have this course")
        if buy_course_data.coupon_id == None:
            buy_course_data.coupon_id = "None"
        return_data.append(
            Bill(
                status=buy_course_data.status,
                user_id=current_user.get_id(),
                course_id=course.get_id(),
                coupon_id=buy_course_data.coupon_id,
                price=course.get_price(),
                discount=discounts,
                amout=course.get_price()-discounts,
                payment=current_user.get_payment_method().get_payment()
            )
        )
        return return_data
        
        
    return result