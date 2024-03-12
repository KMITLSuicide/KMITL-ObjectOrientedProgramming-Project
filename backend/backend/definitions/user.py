import uuid
from typing import List, Union

from pydantic import EmailStr

from backend.definitions.course import Course
from backend.definitions.progress import Progress
from backend.definitions.order import Payment,Order
from backend.definitions.api_data_model import GetOrderData

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

    def search_progress_by_course(self, course: Course):
        for progress in self.__my_progresses:
            course_from_progress = progress.get_course()
            if course_from_progress == course:
                return progress
        return None
    
    def search_progress_by_id(self, progress_id: uuid.UUID):
        return next((progress for progress in self.__my_progresses if isinstance(progress, Progress) and progress.get_id() == progress_id),None)

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
    
    def search_order_by_id(self, order_id:uuid.UUID):
        return next((order for order in self.__orders if order.get_id() == order_id),None)

    def have_access_to_course(self, course: Course):
        for progress in self.__my_progresses:
            if progress.get_course() == course:
                return True
        return False
    
    def have_access_to_courses(self, courses: list[Course]):
        for course in courses:
            if not self.have_access_to_course(course):
                return False
        return True

    def get_courses_without_access(self, courses: list[Course]) -> list[Course]:
        courses_without_access = []
        for course in courses:
            if not self.have_access_to_course(course):
                courses_without_access.append(course)
        return courses_without_access

    def remove_course(self, course:Course):
        progress = self.search_progress_by_course(course)
        if isinstance(progress, Progress):
            self.__my_progresses.remove(progress)
    
    def remove_order(self, order: Order):
        self.__orders.remove(order)

    def try_to_buy_courses(self, courses:list[Course], is_paid: bool, payment_method: Payment, address : str):
        if is_paid:
            progresses = [Progress(course) for course in courses]

            for progress in progresses:
                self.add_progress(progress) 
                self.set_latest_progress(progress) 
        copy_courses = [course for course in courses]
        order = Order(address= address, payment= payment_method, courses= copy_courses, status= is_paid)
        self.__orders.append(order)
        order_data: GetOrderData = GetOrderData(
            id = str(order.get_id()),
            course_list_name=[course.get_name() for course in order.get_courses() if (isinstance(course.get_name(), str))],
            price = order.get_price(),
            address= order.get_address(),
            payment_method= order.get_payment_method().get_name(),
            status= order.get_status(),
            time_stamp= str(order.get_time_stamp().timestamp())
            )
        
        if is_paid:
            courses_in_cart = self.__cart.get_courses()
            self.__cart.remove_courses([course for course in courses_in_cart if course in courses])
        return order_data

    
class Teacher(User):
    def __init__(
        self, name: EmailStr, email: EmailStr, hashed_password: EmailStr
    ) -> None:
        super().__init__(name, email, hashed_password)
        self.__my_teachings: List[Course] = []

    def get_my_teachings(self):
        return self.__my_teachings

    def add_my_teaching(self, course: Course):
        if isinstance(course, Course):
            self.__my_teachings.append(course)
            return True
    def have_access_to_course(self, course: Course):
        
        for my_course in self.get_my_teachings():
            if my_course == course:
                return True
        for progress in self.get_my_progresses():
            if progress.get_course() == course:
                return True
        return False
    
    def remove_course(self, course: Course):
        super().remove_course(course)
        self.__my_teachings.remove(course)

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
    
    def remove_courses(self, courses: list[Course]):
        for course in courses:
            if course in self.__courses:
                self.__courses.remove(course)

