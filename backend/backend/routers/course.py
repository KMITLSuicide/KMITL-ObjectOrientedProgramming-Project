from enum import Enum
from typing import Annotated, List
import uuid
from backend.lib.convert_course_to_card_data import convert_course_to_card_data
from fastapi import APIRouter, Depends, HTTPException, status, Body, Response
from pydantic import BaseModel
import random

from backend.controller_instance import controller
from backend.definitions.course import CourseCategory,CourseReview
from backend.definitions.user import User,Teacher
from backend.definitions.api_data_model import CourseCardData,PostCourseData
from backend.lib.authentication import get_current_user
from pydantic import BaseModel


from backend.definitions.course import (
    Course,

)


router = APIRouter()
route_tags: List[str | Enum] = ["Course"]

class GetAllCourse(BaseModel):
    id: str
    name: str

@router.get("/course", tags=["Debug Purposes"])
def get_all_course():
    return_data: List[CourseCardData] = []
    all_course = controller.get_all_courses()
    for course in all_course:
        return_data.append(
            CourseCardData(
                id = str(course.get_id()),
                name = course.get_name(),
                description = course.get_description(),
                price = course.get_price(),
                rating = course.get_average_rating(),
                banner_image = course.get_banner_image_url()
            ))
    return return_data

@router.post("/course", tags=route_tags)
def new_course(
    post_course_data: Annotated[
        PostCourseData,
        Body(
            examples=[
                {
                    "name": "Example",
                    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                    "price": 100,
                    "category_id": "afeabc96-80f6-4508-82e4-e8a429e86547",
                }
            ],
        ),
    ],
    response: Response,
    current_user: Annotated[User, Depends(get_current_user)],
):
    teacher = current_user

    if not isinstance(teacher, Teacher):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Teacher not found"

    category = controller.search_category_by_id(uuid.UUID(post_course_data.category_id))
    if not category:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Category not found"

    course = Course(
        post_course_data.name,
        post_course_data.description,
        post_course_data.price,
    )

    teacher.add_my_teaching(course)
    category.add_course(course)

    return convert_course_to_card_data(course)


@router.put("/course/{course_id}/edit", tags=["Course"])
def edit_course(
    post_course_data: Annotated[
        PostCourseData,
        Body(
            examples=[
                {
                    "name": "Example",
                    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                    "price": 100,
                    "category_id": "afeabc96-80f6-4508-82e4-e8a429e86547",
                }
            ],
        ),
    ],
    course_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
):
    course = controller.search_course_by_id(uuid.UUID(course_id))
    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    if not isinstance(current_user, Teacher):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User does not have access to course",
        )
    preivous_category = controller.search_category_by_course(course)
    new_category = controller.search_category_by_id(uuid.UUID(post_course_data.category_id))

    if not isinstance(new_category, CourseCategory):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    if not isinstance(preivous_category, CourseCategory):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error, the course is not in",
        )
    result, message  = course.edit(preivous_category,post_course_data.name,post_course_data.description,post_course_data.price,new_category)
    if not result:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )
    return message

@router.delete("/course/{course_id}/delete", tags=["Course"])
def delte_course(
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
    category = controller.search_category_by_course(course)

    if not isinstance(category, CourseCategory):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Category not found",
        )
    user_review = course.search_review_by_user(current_user)

    if isinstance(user_review, CourseReview):
        course.remove_review(user_review)

    current_user.remove_course(course)
