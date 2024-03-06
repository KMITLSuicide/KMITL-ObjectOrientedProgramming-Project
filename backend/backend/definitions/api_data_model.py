from pydantic import BaseModel


class CourseCardData(BaseModel):
    id: str
    name: str
    description: str
    price: float
    rating: float
    banner_image: str
