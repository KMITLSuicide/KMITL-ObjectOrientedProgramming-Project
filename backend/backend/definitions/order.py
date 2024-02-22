class Order:
    def __init__(self) -> None:
        pass

    def create_payment(self):
        pass


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
    def __init__(self, status_input, amount_input, country_input, type_input) -> None:
        self.__status = status_input
        self.__amount = amount_input
        self.__country = country_input
        self.__type = type_input