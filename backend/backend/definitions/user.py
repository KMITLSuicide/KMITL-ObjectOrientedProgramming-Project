from typing import List
import uuid

from backend.definitions.course import Course


class User:
    def __init__(self, name: str, email: str, hashed_password: str) -> None:
        self.__id = uuid.uuid4()
        self.__name = name
        self.__email = email
        self.__hashed_password = hashed_password
        self.__my_learnings: List[Course] = []

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_hashed_password(self):
        return self.__hashed_password

    def get_my_learnings(self):
        return self.__my_learnings

    def add_my_learning(self, course: Course):
        if isinstance(course, Course):
            self.__my_learnings.append(course)
            return True
        return False


class Teacher(User):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.__my_teachings: List[Course] = []

    def get_my_teachings(self):
        return self.__my_teachings

    def add_my_teaching(self, course: Course):
        if isinstance(course, Course):
            self.__my_teachings.append(course)
            return True
        return False
