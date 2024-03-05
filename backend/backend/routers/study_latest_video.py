from enum import Enum
from pydantic import UUID4
from uuid import UUID
from typing import List, Annotated
from fastapi import APIRouter, Response, status, Body, Depends
from backend.definitions.user import User
from backend.lib.authentication import get_current_user
router = APIRouter()

route_tags: List[str | Enum] = ["user"]

@router.get("/user/study_latest_video", tags=route_tags)
async def study_latest_course(current_user: Annotated[User, Depends(get_current_user)]):
    latest_video = current_user.get_latest_video_from_user()
    return latest_video
