class User:
    def __init__(
        self, user_id_input, user_name_input, cart_input, orders_input, my_courses_input
    ) -> None:
        self.__user_id = user_id_input
        self.__user_name = user_name_input
        self.__cart = cart_input
        self.__orders = orders_input
        self.__my_courses = my_courses_input

    def buy_course(self, user_id_input, course_id_input, coupon_id_input):
        pass


class Teacher:
    def __init__(self, my_teaching_course_input) -> None:
        self.__my_teaching_course = my_teaching_course_input

    def add_course(self, course_for_add_input):
        pass
