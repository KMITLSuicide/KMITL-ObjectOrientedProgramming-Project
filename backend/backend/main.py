import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from backend.backend.config import config

from backend.config import API_HOST, API_PORT, LOG_LEVEL
from backend.routers import (
    authentication,
    review,
    buy_course,
    cart,
    course,
    category,
    search,
    list_course_on_home_page,
    list_everything,
    user,
    teacher,
    get_teacher_by_course_id,
    course_material
)

app = FastAPI()

app.include_router(cart.router)
app.include_router(authentication.router)
app.include_router(search.router)
app.include_router(list_course_on_home_page.router)
app.include_router(list_everything.router)
app.include_router(review.router)
app.include_router(course.router)
app.include_router(category.router)
app.include_router(user.router)
app.include_router(buy_course.router)
app.include_router(get_teacher_by_course_id.router)
app.include_router(teacher.router)
# app.include_router(add_coupon.router)
app.include_router(course_material.router)

origins = ["http://localhost:3000", "https://localhost:3000", "*", "http://udemy.acceptablemess.com/", "https://udemy.acceptablemess.com/"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    # print(APP_NAME)
    # print(LOG_LEVEL)
    # print(API_HOST)
    # print(API_PORT)

    uvicorn.run(
        "main:app", host=API_HOST, port=API_PORT, log_level=LOG_LEVEL, reload=True
    )
