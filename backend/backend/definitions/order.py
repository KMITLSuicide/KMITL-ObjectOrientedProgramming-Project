# from backend.definitions.user import User, Teacher
from backend.definitions.course import Course
# from backend.definitions.order import Payment

class Payment:
    def __init__(self, payment_method) -> None:        
        self.__payment_method = payment_method
        
    def get_payment(self):
        return self.__payment_method


class Order:#บิล
    def __init__(self, address, payment:Payment, course:Course, discount, status:bool) -> None:
        self.__address = address
        self.__payment = payment
        self.__course = course
        self.__price = course.get_price()
        self.__discount = discount
        self.__amount = self.__price - self.__discount
        self.__status = status
        
    def get_order(self):
        return self.__address, self.__payment, self.__course, self.__price, self.__discount, self.__amount, self.__status

    def create_payment(self, payment_method):
        payment = Payment(payment_method)
        return payment


class Coupon:
    def __init__(self, coupon_id:str, discount, teacher:"Teacher") -> None:
        self.__coupon_id = coupon_id
        self.__discount = discount
        self.__teacher = teacher
        
    def get_id(self):
        return self.__coupon_id    
        
    def get_discount(self):
        return self.__discount
    
    def get_teacher(self) -> "Teacher":
        return self.__teacher


class CouponCourse(Coupon):
    def __init__(self, coupon_id, discount, teacher, course:Course) -> None:
        super().__init__(coupon_id, discount, teacher)
        self.__course = course
        
    def get_course(self):
        return self.__course

class CouponTeacher(Coupon):
    def __init__(self, coupon_id, discount, teacher) -> None:
        super().__init__(coupon_id, discount, teacher)