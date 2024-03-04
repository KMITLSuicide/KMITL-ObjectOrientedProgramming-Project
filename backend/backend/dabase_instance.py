from backend.controller_instance import controller
from backend.definitions.course import Course, CourseCategory, CourseReview
from backend.definitions.user import User

user_list = [User("Tajdang"), User("user")]

# category and course in that category
category_list = [CourseCategory("category")]

course_list = [Course("course1", "desc", 10000), Course("course2", "desc", 20000)]
for user in user_list:
    print(f"{user.get_name()}: {user.get_id()}")
    controller.add_user(user)

# for category_dict in category_list:
#     for category, courses in category_dict.items():
#         if isinstance(category, CourseCategory):
#             print(category.get_id())
#             for course in courses:
#                 category.add_course(course)
#             controller.add_category(category)

# Assuming you want to print course names, you can loop through courses in each category
for category in controller.get_all_categories():
    print(f"Category: {category.get_id()}")
    for course in category.get_courses():
        print(course.get_name())
