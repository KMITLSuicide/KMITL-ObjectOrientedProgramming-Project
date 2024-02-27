from fastapi import APIRouter, Body
from backend.definitions.course import *
router = APIRouter()

@router.get("/learn_course/")
async def learn_course():
    return "course"
course = Course("Tajdang sud lhor", "This course you will leran how to scam", 300000)
