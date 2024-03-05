from enum import Enum
from uuid import UUID
from typing import List, Annotated
from fastapi import APIRouter, Response, status, Body, Depends
from pydantic import BaseModel
from backend.controller_instance import controller
from backend.definitions.progress import Progress
from backend.definitions.course import Course
from backend.definitions.user import User
from backend.lib.authentication import get_current_user

router = APIRouter()

route_tags: List[str | Enum] = ["user"]

@router.post("/user/enroll_course/{course_id}", tags=route_tags)
def enroll_course(
  course_id: UUID,
  response: Response,
  current_user: Annotated[User, Depends(get_current_user)],
):
  course = controller.search_course_by_id(course_id)
  if not isinstance(course, Course):
    response.status_code = status.HTTP_400_BAD_REQUEST
    return "Error, Course not found"
  user = current_user
  if not isinstance(user, User):
    response.status_code = status.HTTP_400_BAD_REQUEST
    return "Error, User not found"
  new_progress = Progress(course)
  user.add_progress(new_progress)
  user.set_latest_progress(new_progress)
  return user