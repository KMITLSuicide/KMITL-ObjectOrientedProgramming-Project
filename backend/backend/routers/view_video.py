from enum import Enum
from pydantic import UUID4
from uuid import UUID
from typing import List
from fastapi import APIRouter, Body
from backend.controller_instance import controller

router = APIRouter()

route_tags: List[str | Enum] = ["user"]
@router.get("/user/{user_id}/view_video/{video_name}", tags= route_tags)
async def view_video(user_id: UUID4, video_name: str):
    video = controller.view_video_by_name(user_id, video_name)
    return {"video": video}
