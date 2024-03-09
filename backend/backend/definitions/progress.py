from typing import List
from backend.definitions.course import (
    Course,
    CourseMaterialVideo,
    CourseMaterialImage,
    CourseMaterialQuiz,
)
from uuid import UUID


class ProgressVideo():
    def __init__(self, video: CourseMaterialVideo) -> None:
        self.__video = video
        self.__learned = False
    
    def get_video(self):
        return self.__video

    def get_learned(self):
        return self.__learned
    
    def set_learned(self, is_learn:bool):
        self.__learned = is_learn


class ProgressQuiz():
    def __init__(self, quiz: CourseMaterialQuiz) -> None:
        self.__quiz = quiz
        self.__completed = False

    def get_quiz(self):
        return self.__quiz
        
    def get_completed(self):
        return self.__completed
    
    def set_completed(self,is_complete:bool):
        self.__completed = is_complete


class Progress:
    def __init__(self, course: Course) -> None:
        self.__course = course
        self.__name = course.get_name()
        self.__progress_videos: List[ProgressVideo] = []
        self.__progress_quizes: List[ProgressQuiz] = []
        self.__latest_video = None
        self.initialize(course)


    def get_id(self):
        return self.__course.get_id()

    def initialize(self, course: Course):
        self.__progress_videos.extend([ProgressVideo(video) for video in course.get_videos() if isinstance(video, CourseMaterialVideo)])
        self.__progress_quizes.extend([ProgressQuiz(quiz) for quiz in course.get_quizes() if isinstance(quiz, CourseMaterialQuiz)])

    def get_progress_quizes(self):
        return self.__progress_quizes

    def get_progress_videos(self):
        return self.__progress_videos

    def get_course(self):
        return self.__course

    def get_latest_video(self):
        return self.__latest_video

    def get_name(self):
        return self.__name
    

    
    def get_normalized_progress_videos(self, decimal_places=2):
        videos = self.__progress_videos

        if not videos:
            return 0

        learned_videos_count = sum(1 for video in videos if isinstance(video, ProgressVideo) and video.get_learned())

        return round(learned_videos_count / len(videos), decimal_places)


    def get_normalized_progress_quizes(self, decimal_places=2):
        quizes = self.__progress_quizes

        if not quizes:
            return 0

        learned_quizes_count = sum(1 for quiz in quizes if isinstance(quiz, ProgressQuiz) and quiz.get_completed())

        return round(learned_quizes_count / len(quizes), decimal_places)


    def search_video_by_url(self, url: str):
        return next((progress_video for progress_video in self.__progress_videos if isinstance(progress_video, ProgressVideo) and progress_video.get_video().get_url() == url), None)

    def search_video_by_name(self, name: str):
        return next((progress_video for progress_video in self.__progress_videos if isinstance(progress_video, ProgressVideo) and progress_video.get_video().get_name() == name), None)

    def set_learned_video_by_id(self, video_id: UUID, is_learn: bool):
        videos = self.get_progress_videos()

        # Find the video with the specified ID
        matching_video = next((progress_video for progress_video in videos if isinstance(progress_video, ProgressVideo) and progress_video.get_video().get_id() == video_id), None)

        if matching_video:
            # Set the learned status of the found video
            matching_video.set_learned(is_learn)
        else:
            print(f"No video found with ID {video_id}")



    def set_completed_quiz_by_id(self, quiz_id: UUID, is_complete: bool):
        quizzes = self.get_progress_quizes()

        # Find the quiz with the specified ID
        matching_quiz = next((progress_quiz for progress_quiz in quizzes if isinstance(progress_quiz, ProgressQuiz) and progress_quiz.get_quiz().get_id() == quiz_id), None)

        if matching_quiz:
            # Set the completed status of the found quiz
            matching_quiz.set_completed(is_complete)
        else:
            print(f"No quiz found with ID {quiz_id}")


    def set_latest_video(self, progress_video: ProgressVideo):
        return "Invalid, set_latest_video input is not ProgressVideo" if not isinstance(progress_video, ProgressVideo) else setattr(self, '__latest_video', progress_video)

