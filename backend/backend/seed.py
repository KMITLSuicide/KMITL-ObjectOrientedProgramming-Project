from __future__ import annotations
from argon2 import PasswordHasher

from backend.definitions.controller import Controller
from backend.definitions.course import Course, CourseCategory
from backend.definitions.user import Teacher, User

password_hasher = PasswordHasher()


def seed(controller: Controller):
    teachers_name = ["gertrude", "harry", "irene"]
    users_name = ["alice", "bob", "charlie", "david", "eve", "frank"]

    courses = {
        "Programming": [
            Course("Python", "Python programming", 1000),
            Course("Java", "Java programming", 2000),
            Course("C++", "C++ programming", 1500),
            Course("JavaScript", "JavaScript programming", 1800),
        ],
        "Math": [
            Course("Algebra", "Algebra", 1000),
            Course("Calculus", "Calculus", 2000),
            Course("Statistics", "Statistics", 1500),
            Course("Geometry", "Geometry", 1800),
        ],
        "Physics": [
            Course("Thermodynamics", "Thermodynamics", 1800),
            Course("Optics", "Optics", 2200),
            Course("Quantum Mechanics", "Quantum Mechanics", 2500),
            Course("Nuclear Physics", "Nuclear Physics", 2000),
        ],
        "Chemistry": [
            Course("Organic Chemistry", "Organic Chemistry", 1200),
            Course("Inorganic Chemistry", "Inorganic Chemistry", 2200),
            Course("Physical Chemistry", "Physical Chemistry", 1800),
            Course("Analytical Chemistry", "Analytical Chemistry", 2000),
        ],
        "History": [
            Course("World History", "World History", 1200),
            Course("Ancient History", "Ancient History", 1500),
            Course("Modern History", "Modern History", 1800),
            Course("European History", "European History", 2000),
        ],
        "Art": [
            Course("Drawing", "Drawing", 1000),
            Course("Painting", "Painting", 1200),
            Course("Sculpture", "Sculpture", 1500),
            Course("Photography", "Photography", 1800),
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

    for name in users_name:
        controller.add_user(
            User(
                name=name.capitalize(),
                email=f"{name}@example.com",
                hashed_password=password_hasher.hash("password"),
            )
        )

    for category_index, (category, courses) in enumerate(courses.items()):
        category = CourseCategory(name=category)
        for course in courses:
            category.add_course(course)
            teacher_index = category_index % len(teachers_name)
            matched_teachers = controller.search_teacher_by_name(teachers_name[teacher_index].capitalize())
            teacher = matched_teachers[0] if matched_teachers else None
            if isinstance(teacher, Teacher):
                teacher.add_my_teaching(course)
        controller.add_category(category)
