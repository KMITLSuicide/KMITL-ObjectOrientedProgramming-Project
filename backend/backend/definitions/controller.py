from pydantic import UUID4
from typing import List

from backend.definitions.course import Course, CourseCatergory
from backend.definitions.user import Teacher


class Controller:
    def __init__(self) -> None:
        self.__categories: List[CourseCatergory] = []
        self.__teachers: List[Teacher] = []

    def add_category(self, category: CourseCatergory):
        if isinstance(category, CourseCatergory):
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

    def add_teacher(self, teacher: Teacher):
        if isinstance(teacher, Teacher):
            self.__teachers.append(teacher)
            return True
        return False

    def get_all_teacher(self):
        return self.__teachers

    def search_teacher_by_name(self, name: str):
        matched_teachers: List[Teacher] = []
        for teacher in self.__teachers:
            if name in teacher.get_name():
                matched_teachers.append(teacher)
        return matched_teachers
