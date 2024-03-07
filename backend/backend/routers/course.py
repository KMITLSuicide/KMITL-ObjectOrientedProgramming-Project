from enum import Enum
from typing import Annotated, List
import uuid
from fastapi import APIRouter, Depends, HTTPException, status

from backend.controller_instance import controller
from backend.definitions.user import User
from backend.definitions.api_data_model import CourseInfo, CourseLearn, CourseLearnMaterialImage, CourseLearnMaterialQuiz, CourseLearnMaterialQuizQuestions, CourseLearnMaterialVideo
from backend.lib.authentication import get_current_user


router = APIRouter()
route_tags: List[str | Enum] = ["course"]


@router.get("/course", tags=route_tags)
def get_all_course():
    return controller.get_all_courses()


@router.get("/course/{course_id}", tags=route_tags)
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
        rating=0,
        banner_image=course.get_banner_image_url(),
        materials_images=course_materials_images,
        materials_quizes=course_materials_quizes,
        materials_videos=course_materials_videos,
    )
    return course_info


@router.get("/course/{course_id}/learn", tags=route_tags)
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
