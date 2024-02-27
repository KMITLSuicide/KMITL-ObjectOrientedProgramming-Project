from pydantic import UUID4
from typing import List
from uuid import UUID

from backend.definitions.course import Course, CourseCatergory
from backend.definitions.user import Teacher#Question:why don't just collect user
from backend.definitions.user import User

#V commit
from backend.definitions.order import Coupon,CouponCourse,CouponTeacher

class Controller:
    def __init__(self) -> None:
        self.__categories: List[CourseCatergory] = []
        self.__teachers: List[Teacher] = []
        self.__users: List[User] = []#Question: is user going to collect to be Teacher
        self.__coupons: List[Coupon] = [] #V commit

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
    def get_user_by_name(self, name: str):
        matched_users: List[User] = []
        for user in self.__users:
            if name in user.get_name():
                matched_users.append(user)
        return matched_users 
    
    def get_user_by_id(self, user_id: UUID4):
        for user in self.__users:
            if user_id == user.get_id():
                return user
        return "Error: User not found"
    
    def study_latest_video_from_course(self, user_id: str):
        user_id_uuid: UUID4 = UUID(user_id)
        user = self.get_user_by_id(user_id_uuid)
        if isinstance(user, User):
            return user.get_latest_video_from_user()
        else:
            return f"Error: User with ID {user_id} not found "
        
    #V commit
    def search_teacher_by_course(self, course : Course):
        for teacher in self.__teachers:
            if course in teacher.__my_teachings:
                return teacher
        return "Error: Teacher who create this course not found"
    
    #V commit
    def validate_coupon(self, coupon_id: str, course : Course, teacher : Teacher):
        #validate
        if coupon_id != None and course != None and teacher != None:
            #search coupon
            for coupon in self.__coupons :
                if coupon.get_coupon_id() == coupon_id:
                    #check course
                    if(isinstance(coupon, CouponCourse)):
                        if(coupon.get_course() == course):
                            return coupon.get_discount()
                    #check teacher
                    if(isinstance(coupon, CouponTeacher)):
                        if(coupon.get_teacher() == teacher):
                            return coupon.get_discount()
                    else:
                        return f"Error: Coupon ID {coupon.get_coupon_id()} not match with {course.get_name()} or {teacher.get_teacher_name()}"
            return f"Error: Coupon ID {coupon_id} not found"
        else:
            return "Error: Coupon ID or Course or Teacher is invalid"
        
    # def buy_course(self, user_id, course_id, coupon_id): #check out
    #     course = self.search_course_by_id(course_id)
    #     if isinstance(course, Course):
    #         teacher = self.search_teacher_by_course(course)
    #         if isinstance(teacher, Teacher):
    #             discount = 0
    #             if coupon_id != None:
    #                 discount = self.validate_coupon(coupon_id, course, teacher)