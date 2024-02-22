class Course:
    def __init__(self, video_input, quiz_input) -> None:
        self.__video = video_input
        self.__quiz = quiz_input


class Progress:
    def __init__(self) -> None:
        pass


class Category:
    def __init__(self, courses_input) -> None:
        self.__courses = Course

    def get_course_from_course_id_ctgr(self, course_id_input):
        pass
