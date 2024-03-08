from pydantic import UUID4
from typing import List
from uuid import UUID

from backend.definitions.course import Course, CourseCategory
from backend.definitions.user import User, Teacher
from backend.definitions.order import Coupon, CouponCourse, CouponTeacher, Order
from backend.definitions.progress import Progress


class Controller:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Controller, cls).__new__(cls)
            cls._instance.__categories = []
            cls._instance.__users = []
            cls._instance.__teachers = []
            cls._instance.__coupons = []
        return cls._instance

    def __init__(self) -> None:
        self.__categories: List[CourseCategory] = []
        self.__users: List[User] = (
            []
        )  # Question: is user going to collect to be Teacher
        self.__teachers: List[Teacher] = []
        self.__coupons: List[Coupon] = []

    def add_category(self, category: CourseCategory):
        if isinstance(category, CourseCategory):
            self.__categories.append(category)
            return True
        return False

    def get_all_courses(self):
        courses: List[Course] = []
        for category in self.__categories:
            courses.extend(category.get_courses())
        return courses

    def sort_course_by_rating(self):
        all_courses = self.get_all_courses()

        sorted_courses = sorted(
            all_courses, key=lambda course: course.get_average_rating(), reverse=True
        )

        return sorted_courses

    def search_course_by_id(self, uuid: UUID4) -> Course | None:
        for category in self.__categories:
            matched_course = category.search_course_by_id(uuid)
            if matched_course:
                return matched_course
        return None

    def get_all_categories(self):
        return self.__categories

    def search_course_by_name(self, name: str):
        matched_courses: List[Course] = []
        for course in self.get_all_courses():
            if name.lower() in course.get_name().lower():
                matched_courses.append(course)
        return matched_courses

    def search_category_by_id(self, uuid: UUID4):
        for category in self.__categories:
            if category.get_id() == uuid:
                return category
        return None

    def search_category_by_name(self, name: str):
        matched_category: List[CourseCategory] = []
        for category in self.__categories:
            if name.lower() in category.get_name().lower():
                matched_category.append(category)
        return matched_category

    def add_teacher(self, teacher: Teacher):
        if isinstance(teacher, Teacher):
            self.__users.append(teacher)
            return True
        return False

    # Tajdang commit
    def add_user(self, user: User):
        if isinstance(user, User):
            self.__users.append(user)
            return True
        return False

    def get_all_user(self):
        all_user: List[User] = []
        for user in self.__users:
            if isinstance(user, User):
                all_user.append(user)
        return all_user

    def get_all_teacher(self):
        all_teacher: List[Teacher] = []
        for user in self.__users:
            if isinstance(user, Teacher):
                all_teacher.append(user)
        return all_teacher

    def search_user_by_name(self, name: str):
        matched_users: List[User] = []
        for user in self.__users:
            if name in user.get_name():
                matched_users.append(user)
        return matched_users

    def search_teacher_by_name(self, name: str):
        matched_teachers: List[Teacher] = []
        for teacher in self.get_all_teacher():
            if name.lower() in teacher.get_name().lower():
                matched_teachers.append(teacher)
        return matched_teachers

    # Tajdang commit
    def get_users_by_name(self, name: str):
        matched_users: List[User] = []
        for user in self.__users:
            if name == user.get_name():
                matched_users.append(user)
        return matched_users

    def get_user_by_id(self, user_id: UUID4):
        for user in self.__users:
            if user_id == user.get_id():
                return user
        return "Error: User not found"

    def get_teacher_by_name(self, name: str):
        matched_teachers: List[Teacher] = []
        for teacher in self.get_all_teacher():
            if not isinstance(teacher, Teacher):
                return "Error, get_all_teacher func doesnt work"
            if name in teacher.get_name():
                matched_teachers.append(teacher)
        return matched_teachers

    def get_teacher_by_id(self, teacher_id: UUID4):
        for teacher in self.get_all_teacher():
            if not isinstance(teacher, Teacher):
                return "Error, get_all_teacher func doesnt work"
            if teacher_id == teacher.get_id():
                return teacher
        return "Error: Teacher not found"

    def buy_course(self, user: User, status: bool, course_id, coupon_id):

        if status != True:
            return "Error: You haven't paid for course yet"

        if course_id == None:
            return "Error Enter course id"

        course = self.search_course_by_id(course_id)
        if course == None or not isinstance(course, Course):
            return "Error: Course not found"

        teacher = self.search_teacher_by_course(course)
        if teacher == None or not isinstance(teacher, Teacher):
            return "Error: Teacher not found"

        if coupon_id != None:
            coupon = self.search_coupon_by_id(coupon_id)
            if coupon == None or not isinstance(coupon, Coupon):
                return "Error: Coupon not found"

            if not self.validate_coupon(coupon, course, teacher):
                return "Erorr: Coupon is invalid"

            discount = coupon.get_discount()
        if coupon_id == None:
            discount = 0
        self.create_order(user, course, discount, status)
        progress = Progress(course)
        if progress in user.get_my_progresses():
            return "Error: You already have this course"
        user.add_progress(progress)
        user.set_latest_progress(progress)
        return {
            "latest progress": user.get_latest_progress(),
            "user order": user.get_orders(),
        }

    def search_coupon_by_id(self, coupon_id):
        for coupon in self.__coupons:
            if coupon.get_id() == coupon_id:
                return coupon
        return None

    def validate_coupon(self, coupon: Coupon, course: Course, teacher: Teacher):
        if coupon != None:
            if isinstance(coupon, CouponCourse):
                if coupon.get_course() == course:
                    return True
            if isinstance(coupon, CouponTeacher):
                if coupon.get_teacher() == teacher:
                    return True
            return False
        return False

    def search_teacher_by_course(self, course: Course):
        for teacher in self.get_all_teacher():
            if course in teacher.get_my_teachings():
                return teacher
        return None

    def create_order(self, user: User, course, discount, status):
        address = user.get_address()
        payment = user.get_payment_method()
        if payment != None:
            order = Order(address, payment, course, discount, status)
            user.get_orders().append(order)
        return None

    def search_user_by_id(self, user_id):
        for user in self.__users:
            if user.get_id() == user_id:
                return user
        return None

    def search_user_by_email(self, email: str):
        for user in self.__users:
            if email == user.get_email():
                return user

    def add_coupon_course(self, coupon_id, discount, course: Course, teacher: Teacher):
        self.__coupons.append(CouponCourse(coupon_id, discount, course))
        return None

    def add_coupon_teacher(self, coupon_id, discount, teacher: Teacher):
        self.__coupons.append(CouponTeacher(coupon_id, discount, teacher))
        return None

    def get_all_coupons(self):
        return self.__coupons

    def search_category_by_course(self, course: Course):
        for category in self.__categories:
            if course in category.get_courses():
                return category
        return None
