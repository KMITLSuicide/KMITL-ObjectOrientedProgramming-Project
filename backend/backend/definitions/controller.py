from pydantic import UUID4
from typing import List
from uuid import UUID

from backend.definitions.course import Course, CourseCatergory
from backend.definitions.user import Teacher#Question:why don't just collect user
from backend.definitions.user import User
from backend.definitions.order import Coupon, CouponCourse, CouponTeacher, Order, Payment
from backend.definitions.progress import Progress

class Controller:
    def __init__(self) -> None:
        self.__categories: List[CourseCatergory] = []
        self.__teachers: List[Teacher] = []
        self.__users: List[User] = []#Question: is user going to collect to be Teacher
        self.__coupons: List[Coupon] = []

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
        
    def buy_course(self, user:User, status:bool, course_id, coupon_id):
        if status == True:
            course = self.search_course_by_id(course_id)
            coupon = self.search_coupon_by_id(coupon_id)
            if course != None and coupon != None:
                teacher = self.search_teacher_by_course(course)
                if teacher != None:
                    if self.validate_coupon(coupon, course, teacher):
                        discount = coupon.get_discount()
                        self.create_order(user, course, discount, status)
                        progress = Progress(course)
                        user.add_progress(progress)
                        return "Success"
                    return "Erorr: Coupon is invalid"
                return "Error: Teacher not found"
            return "Error: Course or Coupon not found"
        return "Error: You haven't paid for course yet"
        
    def search_coupon_by_id(self, coupon_id):
        for coupon in self.__coupons:
            if coupon.get_id() == coupon_id:
                return coupon
        return None
    
    def validate_coupon(self, coupon:Coupon, course:Course, teacher:Teacher):
        if coupon != None:
            if isinstance(coupon, CouponCourse):
                if coupon.get_course() == course:
                    return True                
            if isinstance(coupon, CouponTeacher):
                if coupon.get_teacher() == teacher:
                    return True
            return False
        return False

    def search_teacher_by_course(self, course:Course):
        for teacher in self.__teachers:
            if course in teacher.get_my_teachings():
                return teacher
        return None
    
    def create_order(self, user:User, course, discount, status):
        address = user.get_address()
        payment = user.get_payment_method()
        if payment != None:
            order = Order(address, payment, course, discount, status)
            user.get_orders().append(order)
        
    
    def search_user_by_id(self, user_id):
        for user in self.__users:
            if user.get_id() == user_id:
                return user
        return None