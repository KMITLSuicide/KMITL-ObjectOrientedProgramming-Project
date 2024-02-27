import uuid
from typing import Annotated, Literal
from pydantic import BaseModel
from fastapi import APIRouter, Body, Response, status

from backend.controller_instance import controller
from backend.definitions.course import Course, CourseCatergory, CourseReview
from backend.definitions.user import User

router = APIRouter()

user = User('user')
controller.add_user(user)
print('user id', user.get_id())
category = CourseCatergory('category')
course = Course('course', 'desc', 10000)
print('course id', course.get_id())
category.add_course(course)
controller.add_category(category)

@router.get("/course/{course_id}/review")
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

@router.post("/course/{course_id}/review")
def create_review(
    course_id: str,
    create_review_post_data: Annotated[
        CreateReviewPostData,
        Body(
            examples=[{
                "user_id": "afeabc96-80f6-4508-82e4-e8a429e86547",
                "star": 5,
                "comment": "very bestest course ever"
            }]
    )],
    response: Response
    ):
    course = controller.search_course_by_id(uuid.UUID(course_id))
    if not isinstance(course, Course):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Course ID not found"
    
    user = controller.get_user_by_id(uuid.UUID(create_review_post_data.user_id))
    if not isinstance(user, User):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "User ID not found"
    
    review = CourseReview(user, create_review_post_data.star, create_review_post_data.comment)
    course.add_review(review)

    return course.get_reviews()
