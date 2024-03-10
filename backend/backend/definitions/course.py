from __future__ import annotations
import uuid
from typing import List, Literal, Optional
from pydantic import UUID4



class QuizQuestion:
    def __init__(self, question: str, correct: bool) -> None:
        self.__id = uuid.uuid4()
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

    def get_id(self):
        return self.__id

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
    def set_name(self, name : str):
        self.__name = name
    
    def set_description(self, description: str):
        self.__description =description


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
    
    def edit(self,name: Optional[str] = None,description: Optional[str] = None,url: Optional[str] = None):
        if name != None:
            super().set_name(name)
        if description != None:
            super().set_description(description)
        if url != None:
            self.__url = url

class CourseMaterialImage(CourseMaterial):  # Question: Is CourseMaterialImage  video?
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
    
    def edit(self,name: Optional[str] = None,description: Optional[str] = None,url: Optional[str] = None):
        if name != None:
            super().set_name(name)
        if description != None:
            super().set_description(description)
        if url != None:
            self.__url = url

class CourseMaterialQuiz(CourseMaterial):
    def __init__(self, name: str, description: str) -> None:
        super().__init__(name, description)
        self.__questions: List[QuizQuestion] = [QuizQuestion("default question", True)]

    def remove_question(self, question: QuizQuestion):
        if isinstance(question, QuizQuestion):
            self.__questions.remove(question)
            return True
        return False

    def add_question(self, question: QuizQuestion):
        if isinstance(question, QuizQuestion):
            self.__questions.append(question)
            return True
        return False
    
    def search_question_by_id(self, id : uuid.UUID):
        return next((quiz for quiz in self.__questions if isinstance(quiz, QuizQuestion) and quiz.get_id() == id), None)

    def get_questions(self):
        return self.__questions
    
    def get_correct_answer(self):
        return [question for question in self.__questions if isinstance(question, QuizQuestion) and question.get_correct()]

    def calculate_normalized_correctness(self, answers: List[QuizQuestion]) -> float:
        correct_answers = self.get_correct_answer()

        if not correct_answers:
            raise ValueError("The quiz has no correct answers. Unable to calculate correctness.")

        correct_count = sum(answer in correct_answers for answer in answers)
        total_correct_answers = len(correct_answers)

        normalized_score = correct_count / total_correct_answers if total_correct_answers > 0 else 0.0
        return normalized_score

    def evaluate_answer(self, answers: List[QuizQuestion]):
        correct_answers = self.get_correct_answer()
        num_correct_answers = len(correct_answers)

        if num_correct_answers == 0:
            return False, "No correct answers available for evaluation."

        # Remove duplicates from user answers
        unique_user_answers = list(set(answers))

        if not unique_user_answers or len(unique_user_answers) != num_correct_answers:
            return False, "Invalid number of unique answers provided for evaluation."

        normalized_correctness = self.calculate_normalized_correctness(unique_user_answers)

        if normalized_correctness == 1:
            return True, "Congratulations! You answered all questions correctly."
        else:
            user_answer_count = int(normalized_correctness * num_correct_answers)
            return False, f"You got {user_answer_count} out of {num_correct_answers} correct answers."

    def is_valid_quiz(self) -> bool:
        correct_count = sum(question.get_correct() for question in self.__questions)

        return correct_count >= 1
    
    def edit_question(self, quiz_question: QuizQuestion, question: Optional[str] = None, correct: Optional[bool] = None):
        if correct is not None:
            quiz_question.set_correct(correct)

            if not self.is_valid_quiz():
                quiz_question.set_correct(not correct)
                return False,"Quiz, must have atleast 1 correct answer"
            
        if question is not None:
            quiz_question.set_question(question)
        return True,"Success"

    def edit(self, name: Optional[str] = None, description: Optional[str] = None):
        if name is not None:
            self._CourseMaterial__name = name
        if description is not None:
            self._CourseMaterial__description = description


        

class CourseReview:
    def __init__(
        self, reviewer: User, star: Literal[1, 2, 3, 4, 5], comment: str
    ) -> None:
        self.__reviewer = reviewer
        self.__star: Literal[1, 2, 3, 4, 5] = star
        self.__comment = comment

    def get_reviewer(self):
        return self.__reviewer

    def get_star(self) -> Literal[1, 2, 3, 4, 5]:
        return self.__star

    def get_comment(self):
        return self.__comment
    
    def set_star(self, star: Literal[1, 2, 3, 4, 5]):
        self.__star = star

    def set_comment(self, comment :str):
        self.__comment = comment

class Course:
    def __init__(
        self, name: str, description: str, price: int
    ) -> None:
        if price < 0:
            price = 0
        self.__id: UUID4 = uuid.uuid4()
        self.__name: str = name
        self.__description: str = description
        self.__price: int = price
        self.__images: List[CourseMaterialImage] = []
        self.__quizes: List[CourseMaterialQuiz] = []
        self.__videos: List[CourseMaterialVideo] = []
        self.__reviews: List[CourseReview] = []
        # Question from Taj to phak: Should I collect latest video to course?
        self.__latest_video = None
        self.__banner_image_url: str = "/course/default-image.jpg"


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

    # Tajdang commit
    def set_latest_video(self, video: CourseMaterialVideo):
        if isinstance(video, CourseMaterialVideo):
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

    # Tajdang commit
    def add_video(self, video: CourseMaterialVideo):
        if isinstance(video, CourseMaterialVideo):
            self.__videos.append(video)
            return True
        return False

    def add_review(self, review: CourseReview):
        if isinstance(review, CourseReview):
            if self.search_review_by_user(review.get_reviewer()):
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

    # Tajdang commit
    def get_latest_video(self):
        return self.__latest_video

    def get_reviews(self):
        return self.__reviews

    def get_banner_image_url(self):
        return self.__banner_image_url
    
    def get_average_rating(self):
        reviews = self.get_reviews()
        
        if not reviews:
            return 0  # or any other default value you prefer
        
        return sum(review.get_star() for review in reviews) / len(reviews)

    def search_review_by_user(self, user: User):
        for review in self.__reviews:
            if review.get_reviewer() == user:
                return review
        return None

    def search_quiz_by_id(self, id: uuid.UUID):
        return next(quiz for quiz in self.__quizes if isinstance(quiz, CourseMaterialQuiz) and quiz.get_id() == id)
    
    def search_video_by_id(self, id: uuid.UUID):
        return next(video for video in self.__videos if isinstance(video, CourseMaterialVideo) and video.get_id() == id)
    
    def search_image_by_id(self, id: uuid.UUID):
        return next(image for image in self.__images if isinstance(image, CourseMaterialImage) and image.get_id() == id)

    def search_video_by_name(self, name: str):
        for video in self.__videos:
            if video.get_name() == name:
                return video
        return None
    
    def remove_review(self, review: CourseReview):
        self.__reviews.remove(review)
    
    def remove_quiz(self, quiz: CourseMaterialQuiz):
        self.__quizes.remove(quiz)

    def remove_video(self, video: CourseMaterialVideo):
        self.__videos.remove(video)
    
    def remove_image(self, image: CourseMaterialImage):
        self.__images.remove(image)

    def edit(self, previous_category : CourseCategory, name:Optional[str]= None, description:Optional[str] = None, price:Optional[int] = None,new_category:Optional[CourseCategory] = None):
        if price is not None:
            if price < 0:
                price = 0
            self.__price = price

        if name is not None:
            self.__name = name

        if description is not None:
            self.__description = description

        
        if new_category is not None:

            if not isinstance(previous_category, CourseCategory):
                return False,"category not found"
            
            previous_category.remove_course(self)

            new_category.add_course(self)

        return True,"edit success"


    


class CourseCategory:
    def __init__(self, name: str) -> None:
        self.__id: UUID4 = uuid.uuid4()
        self.__name: str = name
        self.__courses: List[Course] = []

    def add_course(self, course: Course):
        if isinstance(course, Course):
            self.__courses.append(course)
            return True
        return False

    def remove_course(self, course: Course):
        if isinstance(course, Course):
            self.__courses.remove(course)
            return True
        return False



    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_courses(self):
        return self.__courses

    def search_course_by_id(self, _id: UUID4) -> Course | None:
        for course in self.__courses:
            if course.get_id() == _id:
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
            if course.get_name() == name:
                return course
