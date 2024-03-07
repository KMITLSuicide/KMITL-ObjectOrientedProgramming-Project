from pydantic import BaseModel
from typing import List

class CourseCardData(BaseModel):
    id: str
    name: str
    description: str
    price: float
    rating: float
    banner_image: str
class CategoryInfo(BaseModel):
    id: str
    name: str
    courses: List[CourseCardData]
    
class CourseInfo(BaseModel):
    id: str
    name: str
    description: str
    category_id: str
    category_name: str
    price: float
    rating: float
    banner_image: str
    materials_images: list[str]
    materials_quizes: list[str]
    materials_videos: list[str]

class CourseLearnMaterial(BaseModel):
    id: str
    name: str
    description: str

class CourseLearnMaterialQuizQuestions(BaseModel):
    id: str
    question: str

class CourseLearnMaterialQuiz(CourseLearnMaterial):
    id: str
    name: str
    description: str
    questions: list[CourseLearnMaterialQuizQuestions]

class CourseLearnMaterialImage(CourseLearnMaterial):
    id: str
    name: str
    description: str
    url: str

class CourseLearnMaterialVideo(CourseLearnMaterial):
    id: str
    name: str
    description: str
    url: str

class CourseLearn(CourseInfo):
    learn_materials_quizes: list[CourseLearnMaterialQuiz]
    learn_materials_images: list[CourseLearnMaterialImage]
    learn_materials_videos: list[CourseLearnMaterialVideo]
