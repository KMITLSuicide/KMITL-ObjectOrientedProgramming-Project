from typing import List
from backend.definitions.course import (
    Course,
    CourseMaterialVideo,
    CourseMaterialImage,
    CourseMaterialQuiz,
)


class ProgressVideo(CourseMaterialVideo):
    def __init__(self, video: CourseMaterialVideo) -> None:
        super().__init__(video.get_url(), video.get_name(), video.get_description())
        self.__learned = False


class Progress:
    def __init__(self, course: Course) -> None:
        self.__course = course
        self.__name = course.get_name()
        self.__progress_videos: List[ProgressVideo] = []
        self.__progress_quizes: List[ProgressQuiz] = []
        self.__latest_video = None
        self.initialize(course)

    def get_progress_videos(self):
        return self.__progress_videos

    def get_course(self):
        return self.__course

    def get_latest_video(self):
        return self.__latest_video

    def get_name(self):
        return self.__name

    def search_video_by_url(self, url: str):
        for video in self.__progress_videos:
            if isinstance(video, ProgressVideo):
                if video.get_url() == url:
                    return video
        return None

    def search_video_by_name(self, name: str):
        for video in self.__progress_videos:
            if isinstance(video, ProgressVideo):
                if video.get_name() == name:
                    return video
        return None

    def initialize(self, course: Course):
        for video in course.get_videos():
            if isinstance(video, CourseMaterialVideo):
                self.__progress_videos.append(ProgressVideo(video))
        for quiz in course.get_quizes():
            if isinstance(quiz, CourseMaterialQuiz):
                self.__progress_quizes.append(ProgressQuiz(quiz))

    def set_latest_video(self, video: ProgressVideo):
        if not isinstance(video, ProgressVideo):
            return "Invalid, set_latest_video input is not ProgressVideo"
        self.__latest_video = video


class ProgressQuiz(CourseMaterialQuiz):
    def __init__(self, quiz: CourseMaterialQuiz) -> None:
        super().__init__(quiz.get_name(), quiz.get_description())
        self.__learned = False
