import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from backend.backend.config import config

from backend.config import APP_NAME, API_HOST, API_PORT, LOG_LEVEL
from backend.routers import (
    course_create,
    example,
    info,
    authentication,
    review,
    buy_course,
    course,
    category,
    user,
    search,
    add_course_to_cart,
    list_course_on_home_page,
    list_everything,
    user_post
)

app = FastAPI()

app.include_router(example.router)
app.include_router(info.router)
app.include_router(authentication.router)
app.include_router(search.router)
app.include_router(add_course_to_cart.router)
app.include_router(list_course_on_home_page.router)
app.include_router(list_everything.router)
app.include_router(course_create.router)
# app.include_router(view_my_learning.router)
app.include_router(review.router)
app.include_router(course.router)
app.include_router(category.router)
app.include_router(user.router)
app.include_router(buy_course.router)
app.include_router(user_post.router)

origins = ["http://localhost:3000", "https://localhost:3000", "*"]

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
