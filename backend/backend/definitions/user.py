import uuid
from typing import List, Union

from pydantic import EmailStr

from backend.definitions.course import Course
from backend.definitions.progress import Progress
from backend.definitions.order import Payment,Order,Coupon

class User:
    # Constants
    FETCH_SEARCH_MAX = 10

    def __init__(self, name: str, email: EmailStr, hashed_password: str) -> None:
        self.__id = uuid.uuid4()
        self.__name = name
        self.__email = email
        self.__hashed_password = hashed_password
        self.__my_progresses: List[Progress] = []
        self.__cart: Cart = Cart()
        self.__latest_progress: Union[Progress, None] = None
        self.__address = "thailand"#default is null
        self.__payment_method = Payment("credit cart")
        self.__orders: List[Order] = []

    def get_my_progresses(self):
        return self.__my_progresses

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_hashed_password(self):
        return self.__hashed_password

    def get_cart(self):
        return self.__cart

    def get_latest_video(self):
        if self.__latest_progress is None:
            return None
        latest_progress_video = self.__latest_progress.get_latest_video()
        return latest_progress_video

    def get_latest_progress(self):
        return self.__latest_progress

    def search_progress_by_name(self, name: str):
        for progress in self.__my_progresses:
            if progress.get_name() == name:
                return progress
        return None

    def search_course_by_id(self, course_id: uuid.UUID):
        for progress in self.__my_progresses:
            course = progress.get_course()
            if course.get_id() == course_id:
                return course

    def set_latest_progress(self, progress: Progress):
        self.__latest_progress = progress

    def add_progress(self, progress: Progress):
        self.__my_progresses.append(progress)

    def view_my_learning(self):
        # Fetch at most FETCH_SEARCH_MAX progress items
        return self.__my_progresses[: User.FETCH_SEARCH_MAX]

    def view_video_by_url(self, url: str):
        for progress in self.__my_progresses:
            video = progress.search_video_by_url(url)
            if video != None:
                return video

    def view_video_by_name(self, name: str):
        for progress in self.__my_progresses:
            video = progress.search_video_by_name(name)
            if video != None:
                return video
        return None  # "Video not found please check your input"

    def set_address(self, address):
        self.__address = address

    def set_pament_method(self, payment_method):
        self.__payment_method = payment_method

    def get_address(self):
        return self.__address

    def get_payment_method(self):
        return self.__payment_method

    def get_orders(self):
        return self.__orders

    def have_access_to_course(self, course: Course):
        for progress in self.__my_progresses:
            if progress.get_course() == course:
                return True
        return False


class Teacher(User):
    def __init__(
        self, name: EmailStr, email: EmailStr, hashed_password: EmailStr
    ) -> None:
        super().__init__(name, email, hashed_password)
        self.__my_teachings: List[Course] = []
        self.__my_created_coupons: List[Coupon] = []

    def get_my_teachings(self):
        return self.__my_teachings

    def add_my_teaching(self, course: Course):
        if isinstance(course, Course):
            self.__my_teachings.append(course)
            return True

    def get_my_coupons(self):
        return self.__my_created_coupons

    def have_access_to_course(self, course: Course):
        for my_course in self.get_my_teachings():
            if my_course == course:
                return True
        return False


class Cart:
    def __init__(self):
        self.__courses: list[Course] = []

    def get_courses(self):
        return self.__courses

    def add_course(self, course):
        if isinstance(course, Course):
            self.__courses.append(course)

    def remove_course(self, course):
        self.__courses.remove(course)
