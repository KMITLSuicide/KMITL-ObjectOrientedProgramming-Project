from typing import List, Union
from fastapi import APIRouter, Body
from pydantic import UUID4

from backend.definitions.course import Course
from backend.definitions.user import User, Teacher
from backend.definitions.controller import Controller
from backend.definitions.progress import Progress
from backend.controller_instance import controller

router = APIRouter()

@router.get("/get_teacher_by_course_id/{course_id}",tags= ["Teacher"])
def get_teacher_by_course_id(course_id:UUID4):
  course = controller.search_course_by_id(course_id)
  if course == None:
    return "Error: Course is none"
  for teacher in controller.get_all_teacher():
    for course_in_teacher in teacher.get_my_teachings():
      if course == course_in_teacher:
        return teacher
  return "Error: Teacher not match"