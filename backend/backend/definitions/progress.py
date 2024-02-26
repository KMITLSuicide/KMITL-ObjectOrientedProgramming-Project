from backend.definitions.course import Course
class Progress:
    def __init__(self, course : Course) -> None:
        self.my_course_progress = course
    def get_course(self):
        return self.my_course_progress
    def get_latest_video_from_course(self):
        return self.my_course_progress.get_latest_video
class ProgressVideo(Progress):
    pass
class ProgressQuiz(Progress):
    pass