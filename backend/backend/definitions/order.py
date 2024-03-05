from backend.definitions.user import User
from backend.definitions.course import Course

class Order:
    def __init__(self, address, payment, course:Course, status) -> None:
        self.__address = address
        self.__payment = payment
        self.__course = course
        self.__status = status

    def create_payment(self, status, amount, country, user, payment_method):
        payment = Payment(status, amount, country, user, payment_method)
        return payment


class Coupon:
    def __init__(self, course_input) -> None:
        self.__course = course_input

    def check_course(self, coupon_id_input, course_input):
        pass

    def check_teacher(self, coupon_id_input, teacher_input):
        pass


class CouponCourse:
    def __init__(self, course_input) -> None:
        self.__course = course_input


class CouponTeacher:
    def __init__(self, teacher_input) -> None:
        self.__teacher = teacher_input


class Payment:
    def __init__(self, status, amount, country, user:User, payment_method) -> None:
        self.__status = status
        self.__amount = amount
        self.__country = country
        self.__user = user        
        self.__payment_method = payment_method
        
    def show_payment(self, status, amount, country, user:User, payment_method):
        return f"Status:{status} Amount:{amount} Country:{country} User:{user.get_name()} Payment:{payment_method}"