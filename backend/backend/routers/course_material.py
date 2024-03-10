from enum import Enum
from typing import Annotated, List
import uuid
from fastapi import APIRouter, Depends, HTTPException, status, Body, Response
from pydantic import BaseModel
import random

from backend.controller_instance import controller
from backend.definitions.course import CourseCategory,CourseReview
from backend.definitions.user import User,Teacher
from backend.lib.authentication import get_current_user
from pydantic import BaseModel
from backend.definitions.api_data_model import( 
    CourseInfo, CourseLearn, CourseLearnMaterialImage, 
    CourseLearnMaterialQuiz, CourseLearnMaterialQuizQuestions, 
    CourseLearnMaterialVideo, CourseMaterialData,AddImageToCoursePostData,
    QuizQuestionData,AddQuizToCoursePostData,AddVideoToCoursePostData
    )


from backend.definitions.course import (
    Course,
    CourseMaterialImage,
    CourseMaterialQuiz,
    CourseMaterialVideo,
    QuizQuestion,
)
router = APIRouter()

route_tags: List[str | Enum] = ["Course Material"]

@router.get("/course/{course_id}", tags=["Course Material"])
def get_course_info(course_id: str):
    course = controller.search_course_by_id(uuid.UUID(course_id))
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    category = controller.search_category_by_course(course)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    course_materials_images: list[str] = []
    course_materials_quizes: list[str] = []
    course_materials_videos: list[str] = []

    for image in course.get_images():
        course_materials_images.append(image.get_name())

    for quiz in course.get_quizes():
        course_materials_quizes.append(quiz.get_name())

    for video in course.get_videos():
        course_materials_videos.append(video.get_name())

    course_info: CourseInfo = CourseInfo(
        id=str(course.get_id()),
        name=course.get_name(),
        description=course.get_description(),
        category_name=category.get_name(),
        category_id=str(category.get_id()),
        price=course.get_price(),
        rating= course.get_average_rating(),
        banner_image=course.get_banner_image_url(),
        materials_images=course_materials_images,
        materials_quizes=course_materials_quizes,
        materials_videos=course_materials_videos,
    )
    return course_info


@router.get("/course/{course_id}/learn", tags=["Course Material"])
def get_learn_course_materials(
    course_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
):
    course = controller.search_course_by_id(uuid.UUID(course_id))
    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    if not current_user.have_access_to_course(course):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have access to course",
        )
    course_info = get_course_info(course_id)

    learn_materials_quizes: list[CourseLearnMaterialQuiz] = []
    learn_materials_images: list[CourseLearnMaterialImage] = []
    learn_materials_videos: list[CourseLearnMaterialVideo] = []

    for quiz in course.get_quizes():
        learn_materials_quizes.append(
            CourseLearnMaterialQuiz(
                id=str(quiz.get_id()),
                name=quiz.get_name(),
                description=quiz.get_description(),
                questions=[
                    CourseLearnMaterialQuizQuestions(
                        id=str(question.get_id()),
                        question=question.get_question(),
                    ) for question in quiz.get_questions()
                ]
            )
        )

    for image in course.get_images():
        learn_materials_images.append(
            CourseLearnMaterialImage(
                id=str(image.get_id()),
                name=image.get_name(),
                description=image.get_description(),
                url=image.get_url(),
            )
        )

    for video in course.get_videos():
        learn_materials_videos.append(
            CourseLearnMaterialVideo(
                id=str(video.get_id()),
                name=video.get_name(),
                description=video.get_description(),
                url=video.get_url(),
            )
        )

    course_learn_data = CourseLearn(
        id=course_info.id,
        name=course_info.name,
        description=course_info.description,
        category_name=course_info.category_name,
        category_id=course_info.category_id,
        price=course_info.price,
        rating=course_info.rating,
        banner_image=course_info.banner_image,
        materials_images=course_info.materials_images,
        materials_quizes=course_info.materials_quizes,
        materials_videos=course_info.materials_videos,
        learn_materials_quizes=learn_materials_quizes,
        learn_materials_images=learn_materials_images,
        learn_materials_videos=learn_materials_videos,
    )

    return course_learn_data


@router.post("/course/{course_id}/image", tags=["Image"])
def add_image_to_course(
    course_id: str,
    add_image_to_course_data: Annotated[
        AddImageToCoursePostData,
        Body(
            examples=[
                {
                    "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png",
                    "name": "FastAPI Logo",
                    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                }
            ],
        ),
    ],
    response: Response,
    current_user: Annotated[User, Depends(get_current_user)],
):
    course = controller.search_course_by_id(uuid.UUID(course_id))
    if not isinstance(course, Course):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Course not found"

    if not (current_user == controller.search_teacher_by_course(course)):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "Unauthorized"

    image = CourseMaterialImage(
        add_image_to_course_data.url,
        add_image_to_course_data.name,
        add_image_to_course_data.description,
    )
    course.add_image(image)

    return "success"

@router.put("/course/{course_id}/edit_image/{image_id}", tags=["Image"])
def edit_image(
    course_id: str,
    image_id: uuid.UUID,
    course_material_data: Annotated[
        AddImageToCoursePostData,
        Body(
            examples=[
                {
                    "name": "Which language is FastAPI built with",
                    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                    "url": "fasdfasgadnfaslfd;asdf"
                }
            ],
        ),
    ],
    response: Response,
    current_user: Annotated[User, Depends(get_current_user)],
):
    course = controller.search_course_by_id(uuid.UUID(course_id))
    if not isinstance(course, Course):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Course not found"

    if not (current_user == controller.search_teacher_by_course(course)):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "Unauthorized"

    image = course.search_image_by_id(image_id)

    if not isinstance(image, CourseMaterialImage):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Image not found"

    image.edit(course_material_data.name, course_material_data.description, course_material_data.url)
    return get_learn_course_materials(course_id, current_user)

@router.delete("/course/{course_id}/delete_image/{image_id}", tags=["Image"])
def delete_image(
    course_id: str,
    image_id: uuid.UUID,
    response: Response,
    current_user: Annotated[User, Depends(get_current_user)],
):
    course = controller.search_course_by_id(uuid.UUID(course_id))
    if not isinstance(course, Course):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Course not found"

    if not (current_user == controller.search_teacher_by_course(course)):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "Unauthorized"

    image = course.search_image_by_id(image_id)

    if not isinstance(image, CourseMaterialImage):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "quiz is not instance of CourseMaterialQuiz"

    course.remove_image(image)

    return get_learn_course_materials(course_id, current_user)


@router.post("/course/{course_id}/video", tags=["Video"])
def add_video_to_course(
    course_id: str,
    add_image_to_course_data: Annotated[
        AddVideoToCoursePostData,
        Body(
            examples=[
                {
                    "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png",
                    "name": "FastAPI Logo",
                    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                }
            ],
        ),
    ],
    response: Response,
    current_user: Annotated[User, Depends(get_current_user)],
):
    course = controller.search_course_by_id(uuid.UUID(course_id))
    if not isinstance(course, Course):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Course not found"

    if not (current_user == controller.search_teacher_by_course(course)):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "Unauthorized"

    video = CourseMaterialVideo(
        add_image_to_course_data.url,
        add_image_to_course_data.name,
        add_image_to_course_data.description,
    )
    course.add_video(video)

    return course

@router.put("/course/{course_id}/edit_video/{video_id}", tags=["Video"])
def edit_video(
    course_id: str,
    video_id: uuid.UUID,
    video_data: Annotated[
        AddVideoToCoursePostData,
        Body(
            examples=[
                {
                    "name": "Which language is FastAPI built with",
                    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                    "url": "fasdfasgadnfaslfd;asdf"
                }
            ],
        ),
    ],
    response: Response,
    current_user: Annotated[User, Depends(get_current_user)],
):
    course = controller.search_course_by_id(uuid.UUID(course_id))
    if not isinstance(course, Course):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Course not found"

    if not (current_user == controller.search_teacher_by_course(course)):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "Unauthorized"

    video = course.search_video_by_id(video_id)

    if not isinstance(video, CourseMaterialVideo):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Video not found"

    video.edit(video_data.name, video_data.description, video_data.url)
    return "woohoo"

@router.delete("/course/{course_id}/delete_video/{video_id}", tags=["Video"])
def delete_video(
    course_id: str,
    video_id: uuid.UUID,
    response: Response,
    current_user: Annotated[User, Depends(get_current_user)],
):
    course = controller.search_course_by_id(uuid.UUID(course_id))
    if not isinstance(course, Course):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Course not found"

    if not (current_user == controller.search_teacher_by_course(course)):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "Unauthorized"

    video = course.search_video_by_id(video_id)

    if not isinstance(video, CourseMaterialVideo):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "quiz is not instance of CourseMaterialQuiz"

    course.remove_video(video)

    return get_learn_course_materials(course_id, current_user)

@router.post("/course/{course_id}/quiz", tags=["Quiz"])
def add_quiz_to_course(
    course_id: str,
    add_quiz_to_course_data: Annotated[
        AddQuizToCoursePostData,
        Body(
            examples=[
                {
                    "name": "Which language is FastAPI built with",
                    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                    "questions": [
                        {"question": "Python", "correct": True},
                        {"question": "Rust", "correct": False},
                    ],
                }
            ],
        ),
    ],
    response: Response,
    current_user: Annotated[User, Depends(get_current_user)],
):
    course = controller.search_course_by_id(uuid.UUID(course_id))
    if not isinstance(course, Course):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Teacher not found"

    if not (current_user == controller.search_teacher_by_course(course)):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "Unauthorized"

    quiz = CourseMaterialQuiz(
        add_quiz_to_course_data.name, add_quiz_to_course_data.description
    )
    for question in add_quiz_to_course_data.questions:
        quiz.add_question(QuizQuestion(question.question, question.correct))
    course.add_quiz(quiz)

    return course

@router.put("/course/{course_id}/edit/{quiz_id}", tags=["Quiz"])
def edit_quiz(
    course_id: str,
    quiz_id: uuid.UUID,
    coures_material_data: Annotated[
        CourseMaterialData,
        Body(
            examples=[
                {
                    "name": "Which language is FastAPI built with",
                    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                }
            ],
        ),
    ],
    response: Response,
    current_user: Annotated[User, Depends(get_current_user)],
):
    course = controller.search_course_by_id(uuid.UUID(course_id))
    if not isinstance(course, Course):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Course not found"

    if not (current_user == controller.search_teacher_by_course(course)):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "Unauthorized"

    quiz = course.search_quiz_by_id(quiz_id)

    if not isinstance(quiz, CourseMaterialQuiz):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "quiz is not instance of CourseMaterialQuiz"

    quiz.edit(coures_material_data.name, coures_material_data.description)

    return course

@router.delete("/course/{course_id}/delte/{quiz_id}", tags=["Quiz"])
def delete_quiz(
    course_id: str,
    quiz_id: uuid.UUID,
    response: Response,
    current_user: Annotated[User, Depends(get_current_user)],
):
    course = controller.search_course_by_id(uuid.UUID(course_id))
    if not isinstance(course, Course):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Course not found"

    if not (current_user == controller.search_teacher_by_course(course)):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "Unauthorized"

    quiz = course.search_quiz_by_id(quiz_id)

    if not isinstance(quiz, CourseMaterialQuiz):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "quiz is not instance of CourseMaterialQuiz"

    course.remove_quiz(quiz)

    return course

@router.put("/course/{course_id}/edit/{quiz_id}/edit/{question_id}", tags=["Question"])
def edit_question(
    course_id: str,
    quiz_id: uuid.UUID,
    question_id: uuid.UUID,
    coures_material_data: Annotated[
        QuizQuestionData,
        Body(
            examples=[
                {
                    "question": "Meow Language",
                    "correct": True,
                }
            ],
        ),
    ],
    response: Response,
    current_user: Annotated[User, Depends(get_current_user)],
):
    course = controller.search_course_by_id(uuid.UUID(course_id))
    if not isinstance(course, Course):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Course not found"

    if not (current_user == controller.search_teacher_by_course(course)):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "Unauthorized"

    quiz = course.search_quiz_by_id(quiz_id)

    if not isinstance(quiz, CourseMaterialQuiz):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "quiz not found"
    
    question = quiz.search_question_by_id(quiz_id)

    if not isinstance(question, QuizQuestion):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "question not found"

    success, message = quiz.edit_question(question, coures_material_data.question, coures_material_data.correct)
    if not success:
        response.status_code = status.HTTP_400_BAD_REQUEST
    return message

@router.put("/course/{course_id}/edit/{quiz_id}/add", tags=["Question"])
def add_question(
    course_id: str,
    quiz_id: uuid.UUID,
    coures_material_data: Annotated[
        QuizQuestionData,
        Body(
            examples=[
                {
                    "question": "Meow Language",
                    "correct": True,
                }
            ],
        ),
    ],
    response: Response,
    current_user: Annotated[User, Depends(get_current_user)],
):
    course = controller.search_course_by_id(uuid.UUID(course_id))
    if not isinstance(course, Course):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Course not found"

    if not (current_user == controller.search_teacher_by_course(course)):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "Unauthorized"

    quiz = course.search_quiz_by_id(quiz_id)

    if not isinstance(quiz, CourseMaterialQuiz):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "quiz not found"
    
    return quiz.add_question(QuizQuestion(QuizQuestionData.question, QuizQuestionData.correct))

@router.delete("/course/{course_id}/edit/{quiz_id}/delete/{question_id}", tags=["Question"])
def delte_question(
  course_id: str,
  quiz_id: uuid.UUID,
  question_id: uuid.UUID,
  current_user: Annotated[User, Depends(get_current_user)],
  response: Response
):
  course = controller.search_course_by_id(uuid.UUID(course_id))
  if not isinstance(course, Course):
      response.status_code = status.HTTP_400_BAD_REQUEST
      return "Course not found"

  if not (current_user == controller.search_teacher_by_course(course)):
      response.status_code = status.HTTP_401_UNAUTHORIZED
      return "Unauthorized"

  quiz = course.search_quiz_by_id(quiz_id)

  if not isinstance(quiz, CourseMaterialQuiz):
      response.status_code = status.HTTP_400_BAD_REQUEST
      return "quiz not found"
  
  question = quiz.search_question_by_id(quiz_id)

  if not isinstance(question, QuizQuestion):
      response.status_code = status.HTTP_400_BAD_REQUEST
      return "question not found"

  success = quiz.remove_question(question)
  if not success:
      raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,detail= "How come thid didn't succees")