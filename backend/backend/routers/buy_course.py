from enum import Enum
from uuid import UUID
from typing import List, Annotated, Literal, Annotated
from fastapi import APIRouter, Depends, Response, status, Body, Depends, HTTPException
from pydantic import BaseModel
from backend.controller_instance import controller
from backend.definitions.progress import Progress
from backend.definitions.course import Course
from backend.definitions.order import Payment
from backend.definitions.user import User,Teacher
from backend.lib.authentication import get_current_user
from backend.definitions.api_data_model import PaymentData
router = APIRouter()

route_tags: List[str | Enum] = ["Course"]

class BuyCourseData(BaseModel):
    address: str
    is_paid: bool
    payment_method: str



@router.post("/user/buy/now/{course_id}", tags=route_tags)
def checkout(
    current_user: Annotated[User, Depends(get_current_user)],
    course_id: UUID,
    buy_course_data: Annotated[BuyCourseData, Body(
            examples=[
                {
                    "address": "Thailand",
                    "is_paid": False,
                    "payment_method": "PayPal"
                }
            ]),],
):
    course = controller.search_course_by_id(course_id)
    if not isinstance(course, Course):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Course not found")

    if current_user.have_access_to_course(course):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "User already have the course")

    payment_method = controller.search_payment_by_name(buy_course_data.payment_method)
    if not isinstance(payment_method, Payment):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "Payment method not found")


    return current_user.try_to_buy_courses([course], buy_course_data.is_paid, payment_method, buy_course_data.address)

@router.post("/user/buy/cart", tags=route_tags)
def buy_course_from_cart(
    current_user: Annotated[User, Depends(get_current_user)],
    buy_course_data: Annotated[BuyCourseData, Body(
            examples=[
                {
                    "address": "Thailand",
                    "is_paid": False,
                    "payment_method": "PayPal"
                }
            ]),],
):

    courses = current_user.get_cart().get_courses()

    if not courses:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You don't have any course in the cart")

    for course in courses:
        if current_user.have_access_to_course(course):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already has the course")


    payment_method = controller.search_payment_by_name(buy_course_data.payment_method)
    if not isinstance(payment_method, Payment):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "Payment method not found")


    return current_user.try_to_buy_courses(courses, buy_course_data.is_paid, payment_method, buy_course_data.address)


@router.get('/payment_method',tags= ["Payment Method"])
def get_all_payment_method():
    payments = controller.get_payments()
    return [PaymentData(name=str(payment.get_name()))for payment in payments if isinstance(payment, Payment)]
