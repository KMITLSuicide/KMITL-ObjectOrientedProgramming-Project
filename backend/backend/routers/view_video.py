from fastapi import APIRouter, Body
from backend.controller_instance import controller
router = APIRouter()

@router.get("/view_video/{user_name}/{video_name}")
async def view_video(user_name : str,video_name : str):
    video = controller.view_video_by_name(user_name, video_name)
    return {"video": video
            }