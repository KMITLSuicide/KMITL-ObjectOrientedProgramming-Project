from pydantic import BaseModel


class CourseCardData(BaseModel):
    id: str
    name: str
    description: str
    price: float
    rating: float
    banner_image: str

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
