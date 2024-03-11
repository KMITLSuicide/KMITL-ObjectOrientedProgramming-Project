from __future__ import annotations
from argon2 import PasswordHasher

from backend.config import FRONTEND_URL
from backend.definitions.controller import Controller
from backend.definitions.course import (
    Course,
    CourseCategory,
    CourseMaterialQuiz,
    QuizQuestion,
    CourseMaterialImage,
    CourseMaterialVideo,
)
from backend.definitions.progress import Progress
from backend.definitions.user import User, Teacher
# from backend.definitions.order import Coupon, CouponCourse, CouponTeacher
from typing import Dict, List, Any

password_hasher = PasswordHasher()


def seed(controller: Controller):
    # print('seeding...')
    teachers_name = ["gertrude", "harry", "irene"]
    users_name = ["alice", "bob", "charlie", "david", "eve", "frank"]

    courses = {
        "Programming": [
            {"name": "Python", "description": "Python programming", "price": 1000},
            {"name": "Java", "description": "Java programming", "price": 2000},
            {"name": "C++", "description": "C++ programming", "price": 1500},
            {
                "name": "JavaScript",
                "description": "JavaScript programming",
                "price": 1800,
            },
        ],
        "Math": [
            {"name": "Algebra", "description": "Algebra", "price": 1000},
            {"name": "Calculus", "description": "Calculus", "price": 2000},
            {"name": "Statistics", "description": "Statistics", "price": 1500},
            {"name": "Geometry", "description": "Geometry", "price": 1800},
        ],
        "Physics": [
            {"name": "Thermodynamics", "description": "Thermodynamics", "price": 1800},
            {"name": "Optics", "description": "Optics", "price": 2200},
            {
                "name": "Quantum Mechanics",
                "description": "Quantum Mechanics",
                "price": 2500,
            },
            {
                "name": "Nuclear Physics",
                "description": "Nuclear Physics",
                "price": 2000,
            },
        ],
        "Chemistry": [
            {
                "name": "Organic Chemistry",
                "description": "Organic Chemistry",
                "price": 1200,
            },
            {
                "name": "Inorganic Chemistry",
                "description": "Inorganic Chemistry",
                "price": 2200,
            },
            {
                "name": "Physical Chemistry",
                "description": "Physical Chemistry",
                "price": 1800,
            },
            {
                "name": "Analytical Chemistry",
                "description": "Analytical Chemistry",
                "price": 2000,
            },
        ],
        "History": [
            {"name": "World History", "description": "World History", "price": 1200},
            {
                "name": "Ancient History",
                "description": "Ancient History",
                "price": 1500,
            },
            {"name": "Modern History", "description": "Modern History", "price": 1800},
            {
                "name": "European History",
                "description": "European History",
                "price": 2000,
            },
        ],
        "Art": [
            {"name": "Drawing", "description": "Drawing", "price": 1000},
            {"name": "Painting", "description": "Painting", "price": 1200},
            {"name": "Sculpture", "description": "Sculpture", "price": 1500},
            {"name": "Photography", "description": "Photography", "price": 1800},
        ],
    }

    default_materials = {
        "quizes": [
            {
                "name": "Default Quiz 1",
                "description": "Default Quiz 1 Description",
                "questions": [
                    {"question": "Default Question 1", "correct": True},
                    {"question": "Default Question 2", "correct": False},
                ],
            },
            {
                "name": "Default Quiz 2",
                "description": "Default Quiz 2 Description",
                "questions": [
                    {"question": "Default Question 3", "correct": True},
                    {"question": "Default Question 4", "correct": False},
                ],
            },
        ],
        "images": [
            {
                "url": "/course/default-materials/image1.jpg",
                "name": "Default Image 1",
                "description": "Default Image 1 Description",
            },
            {
                "url": "/course/default-materials/image2.jpg",
                "name": "Default Image 2",
                "description": "Default Image 2 Description",
            },
        ],
        "videos": [
            {
                "url": "/course/default-materials/video1.mp4",
                "name": "Default Video 1",
                "description": "Default Video 1 Description",
            },
            {
                "url": "/course/default-materials/video2.webm",
                "name": "Default Video 2",
                "description": "Default Video 2 Description",
            },
        ],
    }

    for name in teachers_name:
        controller.add_user(
            Teacher(
                name=name.capitalize(),
                email=f"{name}@example.com",
                hashed_password=password_hasher.hash("password"),
            )
        )

    for teacher in controller.get_all_teacher():
        controller.add_coupon_teacher(str(teacher.get_name()), 1000, teacher)

    for name in users_name:
        controller.add_user(
            User(
                name=name.capitalize(),
                email=f"{name}@example.com",
                hashed_password=password_hasher.hash("password"),
            )
        )

    def create_course_materials(course: Course, materials):
        for material_type, materials_list in materials.items():
            if material_type == "quizes":
                for material in materials_list:
                    quiz = CourseMaterialQuiz(
                        name=material["name"],
                        description=material["description"],
                    )
                    for question in material["questions"]:
                        quiz.add_question(
                            QuizQuestion(
                                question["question"],
                                question["correct"],
                            )
                        )
                    course.add_quiz(quiz)
            elif material_type == "images":
                for material in materials_list:
                    course.add_image(
                        CourseMaterialImage(
                            material["url"],
                            material["name"],
                            material["description"],
                        )
                    )
            elif material_type == "videos":
                for material in materials_list:
                    course.add_video(
                        CourseMaterialVideo(
                            material["url"],
                            material["name"],
                            material["description"],
                        )
                    )

    for category_index, (category, courses_list) in enumerate(courses.items()):
        category = CourseCategory(name=category)
        for course_index, course_dict in enumerate(courses_list):
            teacher_index = category_index % len(teachers_name)
            matched_teachers = controller.search_teacher_by_name(
                teachers_name[teacher_index].capitalize()
            )
            teacher = matched_teachers[0] if matched_teachers else None
            if isinstance(teacher, Teacher):
                course = Course(
                    name=course_dict["name"],
                    description=course_dict["description"],
                    price=course_dict["price"]
                )
                teacher.add_my_teaching(course)
                category.add_course(course)
                create_course_materials(course, default_materials)

                user_index = course_index % len(users_name)
                matched_users = controller.search_user_by_name(
                    users_name[user_index].capitalize()
                )
                user = matched_users[0] if matched_users else None
                if isinstance(user, User):
                    user.add_progress(Progress(course))
        controller.add_category(category)
    
    # coupon1 = CouponCourse(c, 999, )