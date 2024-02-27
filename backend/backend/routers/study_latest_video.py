from fastapi import APIRouter, Body
from backend.controller_instance import controller

router = APIRouter()



@router.get("/study_latest_video/{user_name}")
async def study_latest_course(user_name : str):
  user = controller.get_user_by_name(user_name)
  video = controller.study_latest_video_from_course(user_name)
  return {"user" :user, 
          "video":video}

