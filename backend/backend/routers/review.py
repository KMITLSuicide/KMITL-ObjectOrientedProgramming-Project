import uuid
from typing import Annotated, Literal,List
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status, Body, Response

from backend.lib.authentication import get_current_user
from backend.controller_instance import controller
from backend.definitions.course import Course, CourseReview
from backend.definitions.user import User
from enum import Enum

router = APIRouter()

route_tags: List[str | Enum] = ["Reviews"]

@router.get("/course/{course_id}/review", tags = route_tags)
def get_reviews(course_id: str, response: Response):
    return_course: list[GetReviewData] = []
    course = controller.search_course_by_id(uuid.UUID(course_id))
    if not isinstance(course, Course):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Course ID not found"

    for course in course.get_reviews():
        reviewer = course.get_reviewer()
        if not isinstance(reviewer, User):
            return "reviewer is not user"
        return_course.append(
            GetReviewData(
                user_id = str(reviewer.get_id()),
                user_name = reviewer.get_name(),
                star = course.get_star(),
                comment = course.get_comment()
            )
        )
    return return_course


class CreateReviewPostData(BaseModel):
    star: Literal[1, 2, 3, 4, 5]
    comment: str

class GetReviewData(BaseModel):
    user_id:str
    user_name:str
    star: Literal[1, 2, 3, 4, 5]
    comment: str



@router.post("/course/{course_id}/create_review",tags= route_tags)
def create_review(
    course_id: str,
    create_review_post_data: Annotated[
        CreateReviewPostData,
        Body(
            examples=[
                {
                    "star": 5,
                    "comment": "very bestest course ever",
                }
            ]
        ),
    ],
    response: Response,
    current_user: Annotated[User, Depends(get_current_user)],
):
    return_course: list[GetReviewData] = []
    course = controller.search_course_by_id(uuid.UUID(course_id))

    if not isinstance(course, Course):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Course ID not found"
    
    if not current_user.have_access_to_course(course):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have access to course",
        ) 
    
    if create_review_post_data.star not in [1, 2, 3, 4, 5]:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "review range is 1 to 5. Please try again"

    review = CourseReview(
        current_user, create_review_post_data.star, create_review_post_data.comment
    )
    review_adding_result = course.add_review(review)
    if not review_adding_result:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Duplicate reviews"

    for course in course.get_reviews():
        return_course.append(
            GetReviewData(
                user_id= str(current_user.get_id()),
                user_name = current_user.get_name(),
                star = course.get_star(),
                comment = course.get_comment()
            )
        )
    return return_course

@router.put("/course/{course_id}/edit_review",tags= route_tags)
def edit_review(
    course_id: str,
    create_review_post_data: Annotated[
        CreateReviewPostData,
        Body(
            examples=[
                {
                    "star": 5,
                    "comment": "very bestest course ever",
                }
            ]
        ),
    ],
    response: Response,
    current_user: Annotated[User, Depends(get_current_user)],
):
    return_course: list[GetReviewData] = []
    course = controller.search_course_by_id(uuid.UUID(course_id))
    
    if not isinstance(course, Course):
        raise HTTPException(status_code=400, detail="course not found.")  

    if not current_user.have_access_to_course(course):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have access to course",
        )
    
    review = course.search_review_by_user(current_user)

    if not isinstance(review, CourseReview):
        raise HTTPException(status_code=400, detail="You haven't review yet")
    
    if create_review_post_data.star not in [1, 2, 3, 4, 5]:

        response.status_code = status.HTTP_400_BAD_REQUEST
        return "review range is 1 to 5. Please try again"
    
    review.set_star(create_review_post_data.star)
    review.set_comment(create_review_post_data.comment)

    for course in course.get_reviews():
        return_course.append(
            GetReviewData(
                user_id= str(current_user.get_id()),
                user_name = current_user.get_name(),
                star = course.get_star(),
                comment = course.get_comment()
            )
        )
    return return_course

@router.delete("/course/{course_id}/delete_review",tags= route_tags)
def remove_review(current_user: Annotated[User, Depends(get_current_user)], course_id: uuid.UUID):
    return_course: list[GetReviewData] = []
    course = controller.search_course_by_id(course_id)
    if not isinstance(course, Course):
        raise HTTPException(status_code=400, detail="course not found.")  
    
    if not current_user.have_access_to_course(course):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have access to course",
        )
    review = course.search_review_by_user(current_user)

    if not isinstance(review, CourseReview):
        raise HTTPException(status_code=400, detail="You haven't review yet")
    
    course.remove_review(review)

    for course in course.get_reviews():
        return_course.append(
            GetReviewData(
                user_id= str(current_user.get_id()),
                user_name = current_user.get_name(),
                star = course.get_star(),
                comment = course.get_comment()
            )
        )

    return return_course
    
