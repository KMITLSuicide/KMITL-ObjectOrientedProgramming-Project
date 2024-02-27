from fastapi import APIRouter, Body
from backend.controller_instance import controller
router = APIRouter()

@router.get("/view_my_learning/{user_name}")
async def view_my_learning(user_name : str):
    my_progresses = controller.view_my_learning(user_name)
    return {"my_learning": my_progresses}

