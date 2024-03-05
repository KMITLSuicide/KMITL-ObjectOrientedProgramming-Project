import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from backend.backend.config import config
from backend.config import config
from backend.routers import example, info, authentication, review, create_course, view_my_learning, view_video, study_latest_video,buy_course

app = FastAPI()

app.include_router(example.router)
app.include_router(info.router)
app.include_router(authentication.router)
app.include_router(create_course.router)
app.include_router(view_my_learning.router)
app.include_router(view_video.router)
app.include_router(study_latest_video.router)
app.include_router(review.router)
app.include_router(buy_course.router)

origins = [
    "http://localhost:3000",
    "https://localhost:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    print(config.app_name)
    print(config.log_level)
    print(config.api_host)
    print(config.api_port)

    uvicorn.run(
        "main:app",
        host=config.api_host,
        port=config.api_port,
        log_level=config.log_level,
        reload=True
    )
