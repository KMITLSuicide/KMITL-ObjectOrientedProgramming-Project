from fastapi import APIRouter, Body
from backend.controller_instance import controller
from backend.definitions.progress import Progress, ProgressVideo, ProgressQuiz
from backend.definitions.course import Course,CourseCatergory,CourseMaterialVideo

router = APIRouter()



@router.get("/study_latest_video/{user_name}")
async def study_latest_course(user_name : str):
  user = controller.get_user_by_name(user_name)[0]
  latest_video = user.get_latest_video_from_user()
  return {
        "latest_video":latest_video
          }

