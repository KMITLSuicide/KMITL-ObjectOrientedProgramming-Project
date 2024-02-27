import uuid
import uvicorn
from typing import List, Literal, Union, Annotated
from fastapi import FastAPI, Response, status, Body
from pydantic import BaseModel, UUID4

from backend.definitions.controller import Controller
from backend.definitions.user import User, Teacher
from backend.definitions.course import (
    Course,
    CourseCatergory,
    CourseMaterial,
    CourseMaterialImage,
    CourseMaterialQuiz,
    CourseMaterialVideo,
)
from backend.main import controller

app = FastAPI()


class CreateUserData(BaseModel):
    name: str
    type: Union[Literal["User"], Literal["Teacher"]]


@app.post("/user")
def create_user(
    create_user_data: Annotated[
        CreateUserData,
        Body(
            examples=[{"name": "Example"}],
        ),
    ]
):

    if create_user_data.type == "User":
        user = User(create_user_data.name)
    elif create_user_data.type == "Teacher":
        user = Teacher(create_user_data.name)


@app.get("/category")
def get_all_categories():
    return controller.get_all_categories()


class PostCategoryData(BaseModel):
    name: str


@app.post("/category")
def new_category(
    post_category_data: Annotated[
        PostCategoryData,
        Body(
            examples=[{"name": "Example"}],
        ),
    ],
    response: Response,
):
    category = CourseCatergory(post_category_data.name)
    controller.add_category(category)
    return category.get_id()


@app.get("/category/{category_id}")
def get_category_by_id(category_id: str):
    category = controller.search_category_by_id(uuid.UUID(category_id))
    return category


@app.get("/course")
def get_all_course():
    return controller.get_all_courses()


class PostCourseData(BaseModel):
    user_id: str
    name: str
    description: str
    price: int
    category_id: str


@app.post("/course")
def new_course(
    post_course_data: Annotated[
        PostCourseData,
        Body(
            examples=[
                {
                    "user_id": "afeabc96-80f6-4508-82e4-e8a429e86547",
                    "name": "Example",
                    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                    "price": 100,
                    "category_id": "afeabc96-80f6-4508-82e4-e8a429e86547",
                }
            ],
        ),
    ],
    response: Response,
):
    course = Course(
        post_course_data.name, post_course_data.description, post_course_data.price
    )
    category = controller.search_category_by_id(uuid.UUID(post_course_data.category_id))
    if not category:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Category not found"
    category.add_course(course)
    return course.get_id()


@app.get("/course/{course_id}")
def get_course_by_id(course_id: str):
    course = controller.search_course_by_id(uuid.UUID(course_id))
    return course


class CourseMaterialPostData(BaseModel):
    name: str
    description: str


class AddImageToCoursePostData(CourseMaterialPostData):
    url: str
    description: str


@app.post("/course/{course_id}/image")
def add_image_to_course(
    course_id: str,
    add_image_to_course_data: Annotated[
        AddImageToCoursePostData,
        Body(
            examples=[
                {
                    "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png",
                    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                }
            ],
        ),
    ],
):
    course = controller.search_course_by_id(uuid.UUID(course_id))
    return course


class QuizQuestionPostData(BaseModel):
    question: str
    correct: bool


class AddQuizToCoursePostData(CourseMaterialPostData):
    questions: List[QuizQuestionPostData]


@app.post("/course/{course_id}/quiz")
def add_quiz_to_course(
    course_id: str,
    add_image_to_course_data: Annotated[
        AddQuizToCoursePostData,
        Body(
            examples=[
                {
                    "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png",
                    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                }
            ],
        ),
    ],
):
    course = controller.search_course_by_id(uuid.UUID(course_id))
    return course


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")


controller.add_category(CourseCatergory("fgiohklfsghklj"))
