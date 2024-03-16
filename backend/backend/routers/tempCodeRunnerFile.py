def add_course_to_cart(current_user: Annotated[User, Depends(get_current_user)],
                       course_id: str):
    return_cart: list[CourseCardData] = []

    obj_course = controller.search_course_by_id(UUID(course_id))

    if not isinstance(obj_course, Course):
        raise HTTPException(status_code=400,detail= "course not found")#Fail

    obj_cart = current_user.get_cart()

    if obj_course in obj_cart.get_courses():
        raise HTTPException(status_code=400, detail = "This course is in your cart")#Fail

    if(current_user.have_access_to_course(obj_course)):
          raise HTTPException(status_code=400, detail= "You already have this course")#Fail  
    
    obj_cart.add_course(obj_course)

    for course in obj_cart.get_courses():
        return_cart.append(
            CourseCardData(
                id = str(course.get_id()),
                name = course.get_name(),
                description = course.get_description(),
                price = course.get_price(),
                rating = course.get_average_rating(),
                banner_image = course.get_banner_image_url()
        ))
    return return_cart