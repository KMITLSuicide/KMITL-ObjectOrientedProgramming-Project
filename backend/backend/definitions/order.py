#V commit
import uuid
from pydantic import UUID4

class Order:
    def __init__(self, course) -> None:
        self.__course = course

    def create_payment(self ,status, amount, country, type):
        pass


class Coupon:
    def __init__(self, discount: int, coupon_id: str) -> None:
        self.__discount: int = discount
        self.__coupon_id: str = coupon_id

    def check_coupon_course(self, coupon_id, course):
        pass

    def check_coupon_teacher(self, coupon_id, teacher):
        pass

    #V commit
    def get_coupon_id(self):
        return self.__coupon_id

    #V commit
    def get_discount(self) -> int:
        return self.__discount

class CouponCourse(Coupon):
    def __init__(self, discount, coupon_id, course) -> None:
        super().__init__(discount, coupon_id)
        self.__course = course
    
    #V commit
    def get_course(self):
        return self.__course

class CouponTeacher(Coupon):
    def __init__(self, discount,coupon_id, teacher) -> None:
        super().__init__(discount, coupon_id)
        self.__teacher = teacher
        
    #V commit
    def get_teacher(self):
        return self.__teacher


class Payment:
    def __init__(self, status, amount, country, type) -> None:
        self.__status = status
        self.__amount = amount
        self.__country = country
        self.__type = type