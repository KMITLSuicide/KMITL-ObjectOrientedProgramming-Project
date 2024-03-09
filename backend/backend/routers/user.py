from enum import Enum
from uuid import UUID
from typing import List, Annotated, Literal, Annotated
from fastapi import APIRouter, Depends, Response, status, Body, HTTPException
from pydantic import BaseModel

from backend.controller_instance import controller
from backend.definitions.progress import Progress, ProgressQuiz
from backend.definitions.course import Course, CourseMaterialQuiz
from backend.definitions.user import User,Teacher
from backend.lib.authentication import get_current_user
from backend.definitions.api_data_model import CourseCardData, ProgressVideoData, AnswerQuestion
router = APIRouter()
route_tags: List[str | Enum] = ["View Video"]

#Todo return in coursecardmodel

@router.get("/user/learnings", tags=route_tags)
def view_my_learning(current_user : Annotated[User,Depends(get_current_user)]):
    my_progresses = current_user.view_my_learning()
    search_results: List[CourseCardData] = []

    for progresses in my_progresses:
        course = progresses.get_course()
        search_results.append(
            CourseCardData(
                id=str(course.get_id()),
                name=course.get_name(),
                description=course.get_description(),
                price=course.get_price(),
                rating=0,
                banner_image=course.get_banner_image_url(),
            )
        )
    return search_results

@router.get("/user/video_by_name/{video_name}", tags= route_tags)
async def view_video_by_name(current_user: Annotated[User, Depends(get_current_user)], video_name: str):
    video = current_user.view_video_by_name(video_name)
    return {"video": video}

@router.get("/user/latest_video", tags=route_tags)
async def get_latest_video_form_user(current_user: Annotated[User, Depends(get_current_user)]):
    latest_video = current_user.get_latest_video()
    return latest_video


@router.get("/user/search_progression/{course_id}", tags=["Course"])
def search_course_by_id_from_progression(current_user: Annotated[User, Depends(get_current_user)], course_id: UUID):
    course = current_user.search_course_by_id(course_id)
    return course

@router.get("/teacher/my_teaching", tags=["Teacher"])
def get_my_teaching(current_user: Annotated[User, Depends(get_current_user)]):
    search_results: List[CourseCardData] = []

    if not isinstance(current_user, Teacher):
        raise HTTPException(status.HTTP_403_FORBIDDEN, 'Not a teacher')

    for course in current_user.get_my_teachings():
        search_results.append(
            CourseCardData(
                id=str(course.get_id()),
                name=course.get_name(),
                description=course.get_description(),
                price=course.get_price(),
                rating=0,
                banner_image=course.get_banner_image_url(),
            )
        )
    return search_results



@router.get("/user/normalized_videos/{progress_id}", tags=route_tags)
def get_normalized_progress_videos(
    current_user: Annotated[User, Depends(get_current_user)],
    progress_id: UUID
):
    progress = next((progress for progress in current_user.get_my_progresses() if isinstance(progress, Progress) and progress.get_id() == progress_id), None)
    if not isinstance(progress, Progress):
      return "Error, progress_id not found. Please check your progress_id"
    return progress.get_normalized_progress_videos()

@router.post("/user/study_video/{progress_id}", tags=route_tags)
def study_video_by_id(
    current_user: Annotated[User, Depends(get_current_user)],
    progress_id: UUID,
    progress_data : Annotated[ProgressVideoData, Body(
        examples=[
            {
                "id":"adfas",
                "is_complete": True
            }
        ]),],
):
    progress = next((progress for progress in current_user.get_my_progresses() if isinstance(progress, Progress) and progress.get_id() == progress_id), None)
    if not isinstance(progress, Progress):
      return "Error, progress_id not found. Please check your progress_id"
    progress.set_learned_video_by_id(progress_data.id,progress_data.is_complete)

    return progress.get_normalized_progress_videos()


@router.post("/user/complete_quiz_by_id/{progress_id}/{quiz_id}", tags=["Quiz"])
def answer_quiz(
    current_user: Annotated[User, Depends(get_current_user)],
    progress_id: UUID,
    quiz_id: UUID,
    answers_data: Annotated[AnswerQuestion, Body(
        examples=[
            {
                "ids": ["fasdfasdg", "adsfasbasdfsdf"],
            }
        ]
    ), ],
):
    progress = next((progress for progress in current_user.get_my_progresses() if isinstance(progress, Progress) and progress.get_id() == progress_id), None)

    if not isinstance(progress, Progress):
        raise HTTPException(status_code=404, detail="Progress not found. Please check your progress_id")
    
    quiz = next((progress_quiz.get_quiz() for progress_quiz in progress.get_progress_quizes() if isinstance(progress_quiz, ProgressQuiz) and progress_quiz.get_quiz().get_id() == quiz_id), None)

    if not isinstance(quiz, CourseMaterialQuiz):
        raise HTTPException(status_code=404, detail="Quiz not found. Please check your quiz_id")


    answer_list = [quiz.search_question_by_id(answer) for answer in answers_data.ids if quiz.search_question_by_id(answer) in quiz.get_questions()]

    return quiz.evaluate_answer(answer_list)

    
    

class AccountInfo(BaseException):
    type: Literal['user', 'teacher']
    id: str
    name: str
    email: str

@router.get("/account", tags=["User"])
async def get_my_account_info(current_user: Annotated[User, Depends(get_current_user)]):
    user_type = 'user'
    if isinstance(current_user, Teacher):
        user_type = 'teacher'

    return {
        "type": user_type,
        "id": str(current_user.get_id()),
        "name": current_user.get_name(),
        "email": current_user.get_email(),
        }
