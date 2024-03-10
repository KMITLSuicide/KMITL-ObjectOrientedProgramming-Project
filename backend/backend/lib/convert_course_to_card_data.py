from backend.definitions.course import Course


def convert_course_to_card_data(course: Course):
    return {
        "id": str(course.get_id()),
        "name": course.get_name(),
        "description": course.get_description(),
        "price": course.get_price(),
        "rating": course.get_average_rating(),
        "banner_image": course.get_banner_image_url(),
    }