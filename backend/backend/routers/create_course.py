import uuid
from typing import List, Literal, Union, Annotated
from fastapi import APIRouter, Response, status, Body
from pydantic import BaseModel, UUID4

from backend.definitions.controller import Controller
from backend.definitions.user import User, Teacher
from backend.definitions.course import (
    Course,
    CourseCategory,
    CourseMaterial,
    CourseMaterialImage,
    CourseMaterialQuiz,
    CourseMaterialVideo,
    QuizQuestion,
)
from backend.controller_instance import controller


router = APIRouter()


class CreateUserData(BaseModel):
    name: str
    type: Union[Literal["User"], Literal["Teacher"]]


@router.post("/user/create")
def create_user(
    create_user_data: Annotated[
        CreateUserData,
        Body(
            examples=[{"name": "Example", "type": "User"}],
        ),
    ]
):

    if create_user_data.type == "User":
        user = User(create_user_data.name)
        controller.add_user(user)
    elif create_user_data.type == "Teacher":
        user = Teacher(create_user_data.name)
        
        controller.add_user(user)

    return user


@router.get("/category")
def get_all_categories():
    return controller.get_all_categories()


class PostCategoryData(BaseModel):
    name: str


@router.post("/category")
def new_category(
    post_category_data: Annotated[
        PostCategoryData,
        Body(
            examples=[{"name": "Example"}],
        ),
    ],
    response: Response,
):
    category = CourseCategory(post_category_data.name)
    controller.add_category(category)
    return category


@router.get("/category/{category_id}")
def get_category_by_id(category_id: str):
    category = controller.search_category_by_id(uuid.UUID(category_id))
    return category


@router.get("/course")
def get_all_course():
    return controller.get_all_courses()


class PostCourseData(BaseModel):
    teacher_id: str
    name: str
    description: str
    price: int
    category_id: str


@router.post("/course")
def new_course(
    post_course_data: Annotated[
        PostCourseData,
        Body(
            examples=[
                {
                    "teacher_id": "afeabc96-80f6-4508-82e4-e8a429e86547",
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

    teacher = controller.get_teacher_by_id(uuid.UUID(post_course_data.teacher_id))
    if not isinstance(teacher, Teacher):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Teacher not found"

    teacher.add_my_teaching(course)
    category.add_course(course)

    return course


@router.get("/course/{course_id}")
def get_course_by_id(course_id: str):
    course = controller.search_course_by_id(uuid.UUID(course_id))
    return course


class CourseMaterialPostData(BaseModel):
    name: str
    description: str


class AddImageToCoursePostData(CourseMaterialPostData):
    url: str


@router.post("/course/{course_id}/image")
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
):
    course = controller.search_course_by_id(uuid.UUID(course_id))
    if not isinstance(course, Course):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Teacher not found"

    image = CourseMaterialImage(add_image_to_course_data.url, add_image_to_course_data.name, add_image_to_course_data.description)
    course.add_image(image)
    
    return course


class QuizQuestionPostData(BaseModel):
    question: str
    correct: bool


class AddQuizToCoursePostData(CourseMaterialPostData):
    questions: List[QuizQuestionPostData]


@router.post("/course/{course_id}/quiz")
def add_quiz_to_course(
    course_id: str,
    add_quiz_to_course_data: Annotated[
        AddQuizToCoursePostData,
        Body(
            examples=[
                {
                    "name": "Which language is FASTApi built with",
                    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                    "questions": [
                        {
                            "question": "Python",
                            "correct": True
                        },
                        {
                            "question": "Rust",
                            "correct": False
                        }
                    ]
                }
            ],
        ),
    ],
    response: Response
):
    course = controller.search_course_by_id(uuid.UUID(course_id))
    if not isinstance(course, Course):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Teacher not found"

    quiz = CourseMaterialQuiz(add_quiz_to_course_data.name, add_quiz_to_course_data.description)
    for question in add_quiz_to_course_data.questions:
        quiz.add_question(QuizQuestion(question.question, question.correct))
    course.add_quiz(quiz)

    return course


controller.add_category(CourseCategory("fgiohklfsghklj"))
