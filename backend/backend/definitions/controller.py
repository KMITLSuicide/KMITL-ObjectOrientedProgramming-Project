class Controller:
    def __init__(self) -> None:
        self.__users = User
        self.__coupons = Coupon
        self.__payment = Payment
        self.__category = Category
        self.__progress = Progress

    def get_course_from_course_id_ctrl(self, course_id_input):
        pass

    def get_teacher_from_course(self, course_input):
        pass

    def validate_coupon(self, Course_input, coupon_id_input, teacher_input):
        pass

    def create_order(self):
        pass
