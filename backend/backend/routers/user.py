from enum import Enum
from uuid import UUID
from typing import List, Annotated, Literal, Annotated
from fastapi import APIRouter, Depends, Response, status, Body, HTTPException
from pydantic import BaseModel

from backend.controller_instance import controller
from backend.definitions.progress import Progress, ProgressQuiz, ProgressVideo
from backend.definitions.course import Course, CourseMaterialQuiz, QuizQuestion
from backend.definitions.user import User,Teacher
from backend.lib.authentication import get_current_user
from backend.definitions.api_data_model import CourseCardData, ProgressVideoData, ProgressQuizData, AnswerQuestion, GetCorrectAnswer
router = APIRouter()
route_tags: List[str | Enum] = ["Course"]

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
                rating=course.get_average_rating(),
                banner_image=course.get_banner_image_url(),
            )
        )
    return search_results

@router.get("/user/video_by_name/{video_name}", tags= ["Video"])
async def view_video_by_name(current_user: Annotated[User, Depends(get_current_user)], video_name: str):
    video = current_user.view_video_by_name(video_name)
    return {"video": video}

@router.get("/user/latest_video", tags=["Video"])
async def get_latest_video_form_user(current_user: Annotated[User, Depends(get_current_user)]):
    latest_video = current_user.get_latest_video()
    return latest_video


@router.get("/user/search_progression/{course_id}", tags=["Course"])
def search_course_by_id_from_progression(current_user: Annotated[User, Depends(get_current_user)], course_id: UUID):
    course = current_user.search_course_by_id(course_id)
    return course

@router.get("/teacher/teachings", tags=["Course"])
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
                rating=course.get_average_rating(),
                banner_image=course.get_banner_image_url(),
            )
        )
    return search_results



@router.get("/user/normalized_videos/{progress_id}", tags=["Video"])
def get_normalized_progress_videos(
    current_user: Annotated[User, Depends(get_current_user)],
    progress_id: UUID
):
    progress = current_user.search_progress_by_id(progress_id)
    if not isinstance(progress, Progress):
      raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Error, progress_id not found. Please check your progress_id")
    return progress.get_normalized_progress_videos()

@router.get("/user/normalized_quizes/{progress_id}", tags=["Quiz"])
def get_normalized_progress_quizes(
    current_user: Annotated[User, Depends(get_current_user)],
    progress_id: UUID
):
    progress = current_user.search_progress_by_id(progress_id)
    if not isinstance(progress, Progress):
      raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Error, progress_id not found. Please check your progress_id")
    
    return progress.get_normalized_progress_quizes()


@router.get("/user/progress_videos/{progress_id}", tags=["Video"])

def get_progress_videos(current_user: Annotated[User, Depends(get_current_user)],progress_id: UUID):
    progress = current_user.search_progress_by_id(progress_id)
    if not isinstance(progress, Progress):
      raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Error, progress_id not found. Please check your progress_id")
    
    return create_progress_videos_base_model(progress.get_progress_videos())


@router.get("/user/progress_quizes/{progress_id}", tags=["Quiz"])

def get_progress_quizes(current_user: Annotated[User, Depends(get_current_user)],progress_id: UUID):
    progress = current_user.search_progress_by_id(progress_id)
    if not isinstance(progress, Progress):
      raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Error, progress_id not found. Please check your progress_id")
    
    return create_progress_quiz_base_model(progress.get_progress_quizes())

@router.get("/teacher/get_correct_answer/{course_id}/{quiz_id}", tags=["Quiz"])

def get_correct_answer(current_user:Annotated[User, Depends(get_current_user)], course_id: UUID, quiz_id: UUID):
    course = controller.search_course_by_id(course_id)
    if not isinstance(course, Course):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    if not (current_user == controller.search_teacher_by_course(course)):
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail = " Unauthorized")

    quiz = course.search_quiz_by_id(quiz_id)
    
    if not isinstance(quiz, CourseMaterialQuiz):
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "Quiz not found")
    return create_correct_answer_base_model(quiz.get_questions())

@router.put("/user/study_video/{progress_id}", tags=["Video"])
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
    progress = current_user.search_progress_by_id(progress_id)
    if not isinstance(progress, Progress):
      return "Error, progress_id not found. Please check your progress_id"
    progress.set_learned_video_by_id(UUID(progress_data.id),progress_data.is_complete)

    return progress.get_normalized_progress_videos()


@router.put("/user/complete_quiz_by_id/{progress_id}/{quiz_id}", tags=["Quiz"])
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
    )],
):
    progress = find_progress(current_user, progress_id)
    progress_quiz = find_progress_quiz(progress, quiz_id)
    quiz = progress_quiz.get_quiz()

    validate_progress_quiz(progress_quiz)
    validate_quiz(quiz)

    valid_answers = get_valid_answers(quiz, answers_data.ids)

    result, message = quiz.evaluate_answer(valid_answers)

    progress_quiz.set_completed(result)

    return {"result": result, "message": message, "progress_normalized": progress.get_normalized_progress_quizes()}


def find_progress(current_user: User, progress_id: UUID) -> Progress:
    progress = next((p for p in current_user.get_my_progresses() if isinstance(p, Progress) and p.get_id() == progress_id), None)
    if not isinstance(progress, Progress):
        raise HTTPException(status_code=404, detail="Progress not found. Please check your progress_id")
    return progress


def find_progress_quiz(progress: Progress, quiz_id: UUID) -> ProgressQuiz:
    progress_quiz = next((pq for pq in progress.get_progress_quizes() if isinstance(pq, ProgressQuiz) and pq.get_quiz().get_id() == quiz_id), None)
    if not isinstance(progress_quiz, ProgressQuiz):
        raise HTTPException(status_code=404, detail="ProgressQuiz not found. Please check your quiz_id")
    return progress_quiz


def validate_progress_quiz(progress_quiz: ProgressQuiz) -> None:
    if not isinstance(progress_quiz, ProgressQuiz):
        raise HTTPException(status_code=404, detail="Quiz not found. Please check your quiz_id")


def validate_quiz(quiz: CourseMaterialQuiz) -> None:
    if not isinstance(quiz, CourseMaterialQuiz):
        raise HTTPException(status_code=404, detail="Quiz not found. Please check your quiz_id")


def get_valid_answers(quiz: CourseMaterialQuiz, answer_ids: List[UUID]) -> List[QuizQuestion]:
    answer_list = [quiz.search_question_by_id(answer_id) for answer_id in answer_ids]
    valid_answers = [answer for answer in answer_list if answer is not None]

    if len(valid_answers) != len(answer_ids):
        raise HTTPException(status_code=400, detail="Invalid question ID(s) provided.")

    if not valid_answers:
        raise HTTPException(status_code=400, detail="No valid answers found.")

    return valid_answers




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

def create_progress_videos_base_model(videos : list[ProgressVideo]):
    return [
            ProgressVideoData(
            id=str(video.get_id()),
            is_complete=video.get_learned()
        ) for video in videos if isinstance(video, ProgressVideo)
    ]
def create_progress_quiz_base_model(quizes : list[ProgressQuiz]):
    return [
            ProgressQuizData(
            id=str(quiz.get_id()),
            is_complete=quiz.get_completed()
        ) for quiz in quizes if isinstance(quiz, ProgressQuiz)
    ]

def create_correct_answer_base_model(questions: list[QuizQuestion]):
    return [
        GetCorrectAnswer(
            question = question.get_question(),
            correct= question.get_correct(),
            id=str(question.get_id())
        )for question in questions if isinstance(question, QuizQuestion)
    ]