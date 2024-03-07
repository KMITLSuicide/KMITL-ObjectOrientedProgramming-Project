import uuid
from typing import Annotated, Literal,List
from pydantic import BaseModel
from fastapi import APIRouter, Body, Response, status

from backend.controller_instance import controller
from backend.definitions.course import Course, CourseReview
from backend.definitions.user import User
from enum import Enum

router = APIRouter()

route_tags: List[str | Enum] = ["Reviews"]

@router.get("/course/{course_id}/review", tags = route_tags)
def get_reviews(course_id: str, response: Response):
    course = controller.search_course_by_id(uuid.UUID(course_id))
    if not isinstance(course, Course):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Course ID not found"

    return course.get_reviews()


class CreateReviewPostData(BaseModel):
    user_id: str
    star: Literal[1, 2, 3, 4, 5]
    comment: str


@router.post("/course/{course_id}/review", tags = route_tags)
def create_review(
    course_id: str,
    create_review_post_data: Annotated[
        CreateReviewPostData,
        Body(
            examples=[
                {
                    "user_id": "d931c01b-71fa-4df8-93c6-71f05ee077dd",
                    "star": 5,
                    "comment": "very bestest course ever",
                }
            ]
        ),
    ],
    response: Response,
):
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

    return course.get_reviews()
