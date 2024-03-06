from enum import Enum
from typing import List
import uuid
from fastapi import APIRouter

from backend.controller_instance import controller
from backend.definitions.api_data_model import CourseInfo


router = APIRouter()
route_tags: List[str | Enum] = ["course"]


@router.get("/course", tags=route_tags)
def get_all_course():
    return controller.get_all_courses()


@router.get("/course/{course_id}", tags=route_tags)
def get_course_info(course_id: str):
    course = controller.search_course_by_id(uuid.UUID(course_id))
    category = controller.search_category_by_course(course)
    course_materials_images: list[str] = []
    course_materials_quizes: list[str] = []
    course_materials_videos: list[str] = []

    for image in course.get_images():
        course_materials_images.append(
            image.get_name()
        )

    for quiz in course.get_quizes():
        course_materials_quizes.append(
            quiz.get_name()
        )

    for video in course.get_videos():
        course_materials_videos.append(
            video.get_name()
        )

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