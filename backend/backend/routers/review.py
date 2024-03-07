import uuid
from typing import Annotated, Literal
from pydantic import BaseModel
from fastapi import APIRouter, Body, Response, status

from backend.controller_instance import controller
from backend.definitions.course import Course, CourseCategory, CourseReview
from backend.definitions.user import User

router = APIRouter()


@router.get("/course/{course_id}/review")
def get_reviews(course_id: str, response: Response):
    return_course: list[CreateReviewPostData] = []
    course = controller.search_course_by_id(uuid.UUID(course_id))
    if not isinstance(course, Course):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Course ID not found"

    for course in course.get_reviews():
        return_course.append(
            CreateReviewPostData(
                user_id = str(course.get_reviewer().get_id()),
                star = course.get_star(),
                comment = course.get_comment()
            )
        )
    return return_course


class CreateReviewPostData(BaseModel):
    user_id: str
    star: Literal[1, 2, 3, 4, 5]
    comment: str


@router.post("/course/{course_id}/review")
def create_review(
    course_id: str,
    create_review_post_data: Annotated[
        CreateReviewPostData,
        Body(
            examples=[
                {
                    "user_id": "afeabc96-80f6-4508-82e4-e8a429e86547",
                    "star": 5,
                    "comment": "very bestest course ever",
                }
            ]
        ),
    ],
    response: Response,
):
    return_course: list[CreateReviewPostData] = []
    course = controller.search_course_by_id(uuid.UUID(course_id))
    if not isinstance(course, Course):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Course ID not found"

    user = controller.get_user_by_id(uuid.UUID(create_review_post_data.user_id))
    if not isinstance(user, User):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "User ID not found"
    
    review = CourseReview(
        user, create_review_post_data.star, create_review_post_data.comment
    )
    review_adding_result = course.add_review(review)
    if not review_adding_result:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Duplicate reviews"

    for course in course.get_reviews():
        return_course.append(
            CreateReviewPostData(
                user_id = str(course.get_reviewer().get_id()),
                star = course.get_star(),
                comment = course.get_comment()
            )
        )
    return return_course
    