from pydantic import UUID4
from uuid import UUID
from fastapi import APIRouter, Body
from backend.controller_instance import controller
from backend.definitions.progress import Progress, ProgressVideo, ProgressQuiz
from backend.definitions.course import Course, CourseCategory, CourseMaterialVideo

router = APIRouter()


@router.get("/study_latest_video/{user_id}")
async def study_latest_course(user_id: UUID4):
    latest_video = controller.study_latest_video_from_course(user_id)
    return {"latest_video": latest_video}
