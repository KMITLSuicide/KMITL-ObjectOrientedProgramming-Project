from pydantic import UUID4
from uuid import UUID
from fastapi import APIRouter, Body
from backend.controller_instance import controller

router = APIRouter()


@router.get("/view_video/{user_id}/{video_name}")
async def view_video(user_id: UUID4, video_name: str):
    video = controller.view_video_by_name(user_id, video_name)
    return {"video": video}
