from pydantic import UUID4
from uuid import UUID
from fastapi import APIRouter, Body
from backend.controller_instance import controller
router = APIRouter()

@router.get("/view_my_learning/{user_id}")
async def view_my_learning(user_id : UUID4):
    my_progresses = controller.view_my_learning(user_id)
    return {"my_learning": my_progresses}

