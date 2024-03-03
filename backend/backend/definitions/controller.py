from pydantic import UUID4
from typing import List
from uuid import UUID

from backend.definitions.course import Course, CourseCatergory
from backend.definitions.user import Teacher#Question:why don't just collect user
from backend.definitions.user import User


class Controller:
    def __init__(self) -> None:
        self.__categories: List[CourseCatergory] = []
        self.__teachers: List[Teacher] = []
        self.__users: List[User] = []#Question: is user going to collect to be Teacher

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
    
    #Tajdang commit
    def add_user(self, user: User):
        if isinstance(user, User):
            self.__users.append(user)
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
    
    #Tajdang commit
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
        for teacher in self.__teachers:
            if name in teacher.get_name():
                matched_teachers.append(teacher)
        return matched_teachers
    
    def get_teacher_by_id(self, teacher_id: UUID4):
        for teacher in self.__teachers:
            if teacher_id == teacher.get_id():
                return teacher
        return "Error: Teacher not found"
    
    def study_latest_video_from_course(self, user_name: str):
        if self.get_users_by_name(user_name) == []: 
            return None#Name Not found
        user = self.get_users_by_name(user_name)[0]
        if isinstance(user, User):
            return user.get_latest_video_from_user()
        else:
            return f"Error: User with ID {user_name} not found "
        
    #From Taj, cannot view by url because string is too long
    def view_video_by_url(self, user_name: str, url: str):
        if self.get_users_by_name(user_name) == []: 
            return None#Name Not found
        user = self.get_users_by_name(user_name)[0]
        if user == None:
            return "Error: Your username was not found"
        if isinstance(user,User):
            return user.view_video_by_url(url)
        
    def view_video_by_name(self, user_name:str, video_name: str):
        if self.get_users_by_name(user_name) == []: 
            return None#Name Not found
        user = self.get_users_by_name(user_name)[0]
        if isinstance(user,User):
            return user.view_video_by_name(video_name)

    def view_my_learning(self, user_name:str):
        if self.get_users_by_name(user_name) == []: 
            return None#Name Not found
        user = self.get_users_by_name(user_name)[0]
        if isinstance(user,User):
            return user.view_my_learning()
        
    def search_user_by_email(self, email: str):
        for user in self.__users:
            if email == user.get_email():
                return user
            
        for user in self.__teachers:
            if email == user.get_email():
                return user