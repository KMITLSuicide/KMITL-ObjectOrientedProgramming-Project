from fastapi import APIRouter, Body
from backend.definitions.order import Order,Payment

router = APIRouter()

@router.get("/examplerrrr/{status}{amount}{country}{user}{payment_method}")
async def createpayment(status):
    return "hi"

