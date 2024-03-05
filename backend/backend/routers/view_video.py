from enum import Enum
from pydantic import UUID4
from typing import List, Annotated
from fastapi import APIRouter, Response, status, Body, Depends
from uuid import UUID
from typing import List
from fastapi import APIRouter, Body
from backend.controller_instance import controller
from backend.lib.authentication import get_current_user
from backend.definitions.user import User
router = APIRouter()

route_tags: List[str | Enum] = ["user"]
@router.get("/user/view_video/{video_name}", tags= route_tags)
async def view_video(current_user: Annotated[User, Depends(get_current_user)], video_name: str):
    video = current_user.view_video_by_name(video_name)
    return {"video": video}
