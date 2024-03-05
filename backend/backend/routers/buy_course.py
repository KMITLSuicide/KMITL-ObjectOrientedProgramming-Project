from fastapi import APIRouter, Body
from backend.controller_instance import controller
router = APIRouter()

@router.get("/buy_course/{user_name}/{status}/{course_id}/{coupon_id}")
async def buy_course(user_name, status, course_id, coupon_id):
    result = controller.buy_course(user_name, status, course_id, coupon_id)
    return result