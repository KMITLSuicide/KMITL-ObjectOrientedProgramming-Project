
from backend.definitions.course import Course
# from backend.definitions.order import Payment

class Payment:
    def __init__(self, payment_method:str) -> None:        
        self.__payment_method = payment_method
        
    def get_payment(self)->str:
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


