# from backend.definitions.user import User, Teacher
from backend.definitions.course import Course
import uuid
# from backend.definitions.order import Payment

class Payment:
    def __init__(self, name:str) -> None:        
        self.__payment_method = name
        
    def get_name(self)->str:
        return self.__payment_method


class Order:#บิล
    def __init__(self, address, payment:Payment, courses:list[Course], status:bool) -> None:
        self.__id = uuid.uuid4()
        self.__address = address
        self.__payment_method = payment
        self.__courses = courses
        self.__price = sum((course.get_price() for course in courses))
        self.__status = status
        
    def create_payment(self, payment_method):
        payment = Payment(payment_method)
        return payment

    def get_id(self):
        return self.__id

    def get_price(self):
        return self.__price
    
    def get_courses(self):
        return self.__courses
    
    def get_address(self):
        return self.__address
    
    def get_status(self):
        return self.__status
    
    def get_payment_method(self):
        return self.__payment_method

# class Coupon:
#     def __init__(self, coupon_id:str, discount, teacher:"Teacher") -> None:
#         self.__coupon_id = coupon_id
#         self.__discount = discount
#         self.__teacher = teacher
        
#     def get_id(self):
#         return self.__coupon_id    
        
#     def get_discount(self):
#         return self.__discount
    
#     def get_teacher(self) -> "Teacher":
#         return self.__teacher


# class CouponCourse(Coupon):
#     def __init__(self, coupon_id, discount, teacher, course:Course) -> None:
#         super().__init__(coupon_id, discount, teacher)
#         self.__course = course
        
#     def get_course(self):
#         return self.__course

# class CouponTeacher(Coupon):
#     def __init__(self, coupon_id, discount, teacher) -> None:
#         super().__init__(coupon_id, discount, teacher)