import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from backend.backend.config import APP_NAME, API_HOST, API_PORT, LOG_LEVEL
from backend.routers import (
    course_create,
    example,
    info,
    authentication,
    review,
    view_my_learning,
    view_video,
    study_latest_video,
    course,
    category,
    user,
)

app = FastAPI()

app.include_router(example.router)
app.include_router(info.router)
app.include_router(authentication.router)
app.include_router(course_create.router)
app.include_router(view_my_learning.router)
app.include_router(view_video.router)
app.include_router(study_latest_video.router)
app.include_router(review.router)
app.include_router(course.router)
app.include_router(category.router)
app.include_router(user.router)

origins = ["http://localhost:3000", "https://localhost:3000", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    print(APP_NAME)
    print(LOG_LEVEL)
    print(API_HOST)
    print(API_PORT)

    uvicorn.run(
        "main:app", host=API_HOST, port=API_PORT, log_level=LOG_LEVEL, reload=True
    )
