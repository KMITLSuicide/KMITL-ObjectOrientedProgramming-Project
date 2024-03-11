from enum import Enum
from typing import Annotated, List, Sequence
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
    QuizQuestionData,AddQuizToCoursePostData,AddVideoToCoursePostData,
    GetCorrectAnswer
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

    return create_course_info(course)


@router.get("/course/{course_id}/learn", tags=["Debug Purposes"])
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

    if not isinstance(course_info, CourseInfo):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="courseinfo error, please check your course_id",
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
        learn_materials_quizes=create_quizes_base_model(course.get_quizes()),
        learn_materials_images=create_images_base_model(course.get_images()),
        learn_materials_videos=create_videos_base_model(course.get_videos()),
    )

    return course_learn_data
@router.get("/course/{course_id}/image", tags=["Course Material"])
def get_images(course_id:uuid.UUID,current_user: Annotated[User, Depends(get_current_user)]):
    course = controller.search_course_by_id(course_id)

    if not isinstance(course, Course):
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,detail= "course not found")

    if not current_user.have_access_to_course(course):
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,detail= "User doesn't have access")
    return create_course_materials_data(course.get_images())

@router.get("/course/{course_id}/video", tags=["Course Material"])
def get_videos(course_id:uuid.UUID,current_user: Annotated[User, Depends(get_current_user)]):
    course = controller.search_course_by_id(course_id)

    if not isinstance(course, Course):
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,detail= "course not found")

    if not current_user.have_access_to_course(course):
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,detail= "User doesn't have access")
    return create_course_materials_data(course.get_videos())

@router.get("/course/{course_id}/quiz", tags=["Course Material"])
def get_quizes(course_id:uuid.UUID,current_user: Annotated[User, Depends(get_current_user)]):
    course = controller.search_course_by_id(course_id)

    if not isinstance(course, Course):
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,detail= "course not found")

    if not current_user.have_access_to_course(course):
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,detail= "User doesn't have access")
    return create_course_materials_data(course.get_quizes())

@router.get("/course/{course_id}/image/{image_id}", tags=["Image"])
def get_image(course_id:uuid.UUID, image_id : uuid.UUID,current_user: Annotated[User, Depends(get_current_user)]):
    course = controller.search_course_by_id(course_id)
    if not isinstance(course, Course):
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,detail= "course not found")
    image = course.search_image_by_id(image_id)
    if not isinstance(image, CourseMaterialImage):
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail=" image not found")

    if not current_user.have_access_to_course(course):
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,detail= "User doesn't have access")
    course_learn_image: CourseLearnMaterialImage = CourseLearnMaterialImage(
                id=str(image.get_id()),
                name=image.get_name(),
                description=image.get_description(),
                url=image.get_url(),
            )

    return  course_learn_image


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

    return str(image.get_id())

@router.put("/course/{course_id}/image/{image_id}", tags=["Image"])
def edit_image(
    course_id: str,
    image_id: uuid.UUID,
    course_material_data: Annotated[
        AddImageToCoursePostData,
        Body(
            examples=[
                {
                    "name": "meow image",
                    "description": "Meow twerking is super fun",
                    "url": "tajdang.com"
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
    return get_image(uuid.UUID(course_id), image_id,current_user)

@router.delete("/course/{course_id}/image/{image_id}", tags=["Image"])
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
        return "Image not found"

    course.remove_image(image)

    return get_learn_course_materials(course_id, current_user)


@router.get("/course/{course_id}/video/{video_id}", tags=["Video"])
def get_video(course_id:uuid.UUID, video_id : uuid.UUID,current_user: Annotated[User, Depends(get_current_user)]):
    course = controller.search_course_by_id(course_id)
    if not isinstance(course, Course):
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,detail= "course not found")
    video = course.search_video_by_id(video_id)
    if not isinstance(video, CourseMaterialVideo):
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail=" video not found")

    if not current_user.have_access_to_course(course):
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,detail= "User doesn't have access")

    course_learn_video: CourseLearnMaterialVideo = CourseLearnMaterialVideo(
                            id=str(video.get_id()),
                            name=video.get_name(),
                            description=video.get_description(),
                            url=video.get_url(),
                        )
    return course_learn_video

@router.post("/course/{course_id}/video", tags=["Video"])
def add_video_to_course(
    course_id: str,
    add_image_to_course_data: Annotated[
        AddVideoToCoursePostData,
        Body(
            examples=[
                {
                    "url": "https://youtube.com",
                    "name": "youtbe",
                    "description": "add video",
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

    return str(video.get_id())

@router.put("/course/{course_id}/video/{video_id}", tags=["Video"])
def edit_video(
    course_id: str,
    video_id: uuid.UUID,
    video_data: Annotated[
        AddVideoToCoursePostData,
        Body(
            examples=[
                {
                    "name": "Tajdang dance clip",
                    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                    "url": "Phuwit.com"
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
    return get_video(uuid.UUID(course_id), video_id,current_user)

@router.delete("/course/{course_id}/video/{video_id}", tags=["Video"])
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
        return "Video is not found"

    course.remove_video(video)

    return get_learn_course_materials(course_id, current_user)

@router.get("/course/{course_id}/quiz/{quiz_id}", tags=["Quiz"])
def get_quiz(course_id:uuid.UUID, quiz_id : uuid.UUID,current_user: Annotated[User, Depends(get_current_user)]):
    course = controller.search_course_by_id(course_id)
    if not isinstance(course, Course):
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,detail= "course not found")

    quiz = course.search_quiz_by_id(quiz_id)
    if not isinstance(quiz, CourseMaterialQuiz):
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="quiz  not found")

    if not current_user.have_access_to_course(course):
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,detail= "User doesn't have access")

    course_learn_quiz : CourseLearnMaterialQuiz=  CourseLearnMaterialQuiz(
                id=str(quiz.get_id()),
                name=quiz.get_name(),
                description=quiz.get_description(),
                questions= [
                    CourseLearnMaterialQuizQuestions(
                    id=str(question.get_id()),
                    question=question.get_question(),
                    ) for question in quiz.get_questions()]
            )
    return course_learn_quiz

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

    return str(quiz.get_id())

@router.put("/course/{course_id}/quiz/{quiz_id}", tags=["Quiz"])
def edit_quiz(
    course_id: str,
    quiz_id: uuid.UUID,
    coures_material_data: Annotated[
        CourseMaterialData,
        Body(
            examples=[
                {
                    "name": "Is Tajdang the smartest guy in the world?",
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
        return "quiz not found"

    quiz.edit(coures_material_data.name, coures_material_data.description)

    return get_quiz(uuid.UUID(course_id), quiz_id, current_user)

@router.delete("/course/{course_id}/quiz/{quiz_id}", tags=["Quiz"])
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
        return "quiz not found"

    course.remove_quiz(quiz)

    return get_learn_course_materials(course_id, current_user)


@router.get("/course/{course_id}/quiz/{quiz_id}/question/{question_id}", tags=["Question"])
def get_question(
  course_id: str,
  quiz_id: uuid.UUID,
  question_id: uuid.UUID,
  current_user: Annotated[User, Depends(get_current_user)],
):
    course = controller.search_course_by_id(uuid.UUID(course_id))
    if not isinstance(course, Course):
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST)

    if not current_user.have_access_to_course(course):
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,detail= "User doesn't have access")


    quiz = course.search_quiz_by_id(quiz_id)

    if not isinstance(quiz, CourseMaterialQuiz):
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST)


    question = quiz.search_question_by_id(question_id)
    if not isinstance(question, QuizQuestion):
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="question not found")

    question_learn = CourseLearnMaterialQuizQuestions(id = str(question.get_id()),question= question.get_question())

    return question_learn




@router.put("/course/{course_id}/quiz/{quiz_id}/question/{question_id}", tags=["Question"])
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

    question = quiz.search_question_by_id(question_id)

    if not isinstance(question, QuizQuestion):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "question not found"

    success, message = quiz.edit_question(question, coures_material_data.question, coures_material_data.correct)
    if not success:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return message
    return get_question(course_id,quiz_id,question.get_id(),current_user)

@router.post("/course/{course_id}/quiz/{quiz_id}/question", tags=["Question"])
def add_question(
    course_id: str,
    quiz_id: uuid.UUID,
    quiz_material_data: Annotated[
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

    question = QuizQuestion(quiz_material_data.question, quiz_material_data.correct)
    quiz.add_question(question)
    return get_question(course_id, quiz_id, question.get_id(), current_user)

@router.delete("/course/{course_id}/quiz/{quiz_id}/question/{question_id}", tags=["Question"])
def delete_question(
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

    question = quiz.search_question_by_id(question_id)

    if not isinstance(question, QuizQuestion):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "question not found"

    success, message = quiz.remove_question(question)
    if not success:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= message)
    return get_learn_course_materials(course_id, current_user)

def create_images_base_model(images : list[CourseMaterialImage]):
    return [
            CourseLearnMaterialImage(
            id=str(image.get_id()),
            name=image.get_name(),
            description=image.get_description(),
            url=image.get_url(),
        ) for image in images if isinstance(image, CourseMaterialImage)
    ]
def create_videos_base_model(videos : list[CourseMaterialVideo]):
    return [
            CourseLearnMaterialVideo(
            id=str(video.get_id()),
            name=video.get_name(),
            description=video.get_description(),
            url=video.get_url(),
        ) for video in videos if isinstance(video, CourseMaterialVideo)
    ]
def create_quizes_base_model(quizes : list[CourseMaterialQuiz]):
    return [
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
        ) for quiz in quizes if isinstance(quiz, CourseMaterialQuiz)
    ]



def create_course_info(course: Course):
    category = controller.search_category_by_course(course)
    if not isinstance(category, CourseCategory):
        return "What there is no way"
    course_info: CourseInfo = CourseInfo(
        id=str(course.get_id()),
        name=course.get_name(),
        description=course.get_description(),
        category_name=category.get_name(),
        category_id=str(category.get_id()),
        price=course.get_price(),
        rating= course.get_average_rating(),
        banner_image=course.get_banner_image_url(),
        materials_images=[image.get_name() for image in course.get_images()],
        materials_quizes=[quiz.get_name() for quiz in course.get_quizes()],
        materials_videos=[video.get_name() for video in course.get_videos()],
    )
    return course_info

class EachCourseMaterialData(BaseModel):
    id: str
    name :str


def create_course_materials_data(course_material_list: Sequence[CourseMaterialImage | CourseMaterialVideo | CourseMaterialQuiz]):
    # Check if all elements in the list have the same type
    if not all(type(course_material) == type(course_material_list[0]) for course_material in course_material_list):
        raise TypeError("All elements in the list must be of the same type")

    return [
        EachCourseMaterialData(id=str(course_material.get_id()), name=course_material.get_name()) for course_material in course_material_list
    ]