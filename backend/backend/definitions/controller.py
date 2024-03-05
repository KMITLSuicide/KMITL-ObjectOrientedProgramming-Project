from pydantic import UUID4
from typing import List
from uuid import UUID

from backend.definitions.course import Course, CourseCategory
from backend.definitions.user import Teacher  # Question:why don't just collect user
from backend.definitions.user import User


class Controller:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Controller, cls).__new__(cls)
            cls._instance.__categories = []
            cls._instance.__users = []
        return cls._instance

    def __init__(self) -> None:
        self.__categories: List[CourseCategory] = []
        self.__users: List[User] = (
            []
        )  # Question: is user going to collect to be Teacher

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

    def search_course_by_id(self, uuid: UUID4) -> Course | None:
        for category in self.__categories:
            matched_course = category.search_course_by_id(uuid)
            if matched_course:
                return matched_course
        return None

    def search_course_by_name(self, name: str):
        matched_courses: List[Course] = []
        for course in self.get_all_courses():
            if name in course.get_name():
                matched_courses.append(course)
        return matched_courses

    def get_all_categories(self):
        return self.__categories

    def search_category_by_id(self, uuid: UUID4):
        for category in self.__categories:
            if category.get_id() == uuid:
                return category
        return None

    def search_category_by_name(self, name: str):
        for category in self.__categories:
            if category.get_name() == name:
                return category
        return None

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

    def search_teacher_by_name(self, name: str):
        matched_teachers: List[Teacher] = []
        for teacher in self.get_all_teacher():
            if not isinstance(teacher, Teacher):
                return "Error, get_all_teacher func doesnt work"
            if name in teacher.get_name():
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

    def study_latest_video_from_course(self, user_id: UUID4):
        if self.get_user_by_id(user_id) == None:
            return f"Error user with user id {user_id} is not found "
        user = self.get_user_by_id(user_id)
        if isinstance(user, User):
            print(user.get_id())
            return user.get_latest_video_from_user()

    # From Taj, cannot view by url because string is too long
    def view_video_by_url(self, user_id: UUID4, url: str):
        if self.get_user_by_id(user_id) == None:
            return f"Error user with user id {user_id} is not found "
        user = self.get_user_by_id(user_id)
        if isinstance(user, User):
            return user.view_video_by_url(url)

    def view_video_by_name(self, user_id: UUID4, video_name: str):
        if self.get_user_by_id(user_id) == None:
            return f"Error user with user id {user_id} is not found "
        user = self.get_user_by_id(user_id)
        if isinstance(user, User):
            return user.view_video_by_name(video_name)

    def view_my_learning(self, user_id: UUID4):
        if self.get_user_by_id(user_id) == None:
            return f"Error user with user id {user_id} is not found "
        user = self.get_user_by_id(user_id)
        if isinstance(user, User):
            return user.view_my_learning()

    def search_user_by_email(self, email: str):
        for user in self.__users:
            if email == user.get_email():
                return user

        for user in self.get_all_teacher():
            if email == user.get_email():
                return user
