from __future__ import annotations
import uuid
from typing import List, Literal
from pydantic import UUID4


class QuizQuestion:
    def __init__(self, question: str, correct: bool) -> None:
        self.__question = question
        self.__correct = correct

    def set_question(self, question: str):
        if isinstance(question, str):
            self.__question = question
            return True
        return False

    def set_correct(self, correct: bool):
        if isinstance(correct, bool):
            self.__correct = correct
            return True
        return False

    def get_question(self):
        return self.__question

    def get_correct(self):
        return self.__correct


class CourseMaterial:
    def __init__(self, name: str, description: str) -> None:
        self.__id: UUID4 = uuid.uuid4()
        self.__name: str = name
        self.__description: str = description

    def get_id(self):
        return self.__id
    
    def get_name(self):
        return self.__name
    
    def get_description(self):
        return self.__description


class CourseMaterialVideo(CourseMaterial):
    def __init__(self, url: str, name: str, description: str) -> None:
        super().__init__(name, description)
        self.__url: str = url

    def set_url(self, url: str):
        if isinstance(url, str):
            self.__url = url
            return True
        return False

    def get_url(self):
        return self.__url

class CourseMaterialImage(CourseMaterial):#Question: Is CourseMaterialImage  video?
    def __init__(self, url: str, name: str, description: str) -> None:
        super().__init__(name, description)
        self.__url: str = url

    def set_url(self, url: str):
        if isinstance(url, str):
            self.__url = url
            return True
        return False

    def set_description(self, description: str):
        if isinstance(description, str):
            self.__description = description
            return True
        return False

    def get_url(self):
        return self.__url

    def get_description(self):
        return self.__description


class CourseMaterialQuiz(CourseMaterial):
    def __init__(self, name: str, description: str) -> None:
        super().__init__(name, description)
        self.__questions: List[QuizQuestion] = []

    def add_question(self, question: QuizQuestion):
        if isinstance(question, QuizQuestion):
            self.__questions.append(question)
            return True
        return False

    def get_questions(self):
        return self.__questions


class CourseReview:
    def __init__(self, reviewer: User, star: Literal[1, 2, 3, 4, 5], comment: str) -> None:
        self.__reviewer = reviewer
        self.__star = star
        self.__comment = comment
        
    def get_reviewer(self):
        return self.__reviewer

    def get_star(self):
        return self.__star

    def get_comment(self):
        return self.__comment


class Course:
    def __init__(self, name: str, description: str, price: int) -> None:
        self.__id: UUID4 = uuid.uuid4()
        self.__name: str = name
        self.__description: str = description
        self.__price: int = price
        self.__images: List[CourseMaterialImage] = []
        self.__quizes: List[CourseMaterialQuiz] = []
        self.__videos: List[CourseMaterialVideo] = []
        self.__reviews: List[CourseReview] = []
        #Question from Taj to phak: Should I collect latest video to course?
        self.__latest_video = None
    
    def set_name(self, name: str):
        if isinstance(name, str):
            self.__name = name
            return True
        return False

    def set_description(self, description: str):
        if isinstance(description, str):
            self.__description = description
            return True
        return False

    def set_price(self, price: int) -> bool:
        if isinstance(price, int):
            self.__price = price
            return True
        return False

    #Tajdang commit
    def set_latest_video(self, video: CourseMaterialVideo):
        if(isinstance(video, CourseMaterialVideo)):
            self.__latest_video = video
            return True
        return False
    
    def add_image(self, image: CourseMaterialImage):
        if isinstance(image, CourseMaterialImage):
            self.__images.append(image)
            return True
        return False

    def add_quiz(self, quiz: CourseMaterialQuiz):
        if isinstance(quiz, CourseMaterialQuiz):
            self.__quizes.append(quiz)
            return True
        return False

    #Tajdang commit
    def add_videos(self, video: CourseMaterialVideo):
        if(isinstance(video, CourseMaterialVideo)):
            self.__videos.append(video)
            return True
        return False

    def add_review(self, review: CourseReview):
        if(isinstance(review, CourseReview)):
            if(self.search_review_by_user(review.get_reviewer())):
                return False
            self.__reviews.append(review)
            return True
        return False

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def get_price(self):
        return self.__price

    def get_images(self):
        return self.__images

    def get_quizes(self):
        return self.__quizes
    
    def get_videos(self):
        return self.__videos
    #Tajdang commit
    def get_latest_video(self):
        return self.__latest_video

    def get_reviews(self):
        return self.__reviews
    
    def search_review_by_user(self, user: User):
        for review in self.__reviews:
            if (review.get_reviewer() == user):
                return review
        return None

    def search_video_by_name(self,name : str):
        for video in self.__videos:
            if(video.__name == name):
                return video
        return None
    

class CourseCatergory:
    def __init__(self, name: str) -> None:
        self.__id: UUID4 = uuid.uuid4()
        self.__name: str = name
        self.__courses: List[Course] = []

    def add_course(self, course: Course):
        if isinstance(course, Course):
            self.__courses.append(course)
            return True
        return False

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_courses(self):
        return self.__courses

    def search_course_by_id(self, id: UUID4) -> Course | None:
        for course in self.__courses:
            if course.get_id() == id:
                return course
        return None
    
    def search_course_by_name(self, name: str):
        matched_courses: List[Course] = []
        for course in self.__courses:
            if course.get_name().find(name):
                matched_courses.append(course)
        return matched_courses
    def get_first_course_by_name(self, name: str):
        for course in self.__courses:
            if(course.get_name() == name):
                return course
