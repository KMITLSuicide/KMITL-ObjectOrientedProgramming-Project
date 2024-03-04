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
            Course("Python", "Python programming", 10000),
            Course("Java", "Java programming", 20000),
            Course("C++", "C++ programming", 15000),
            Course("JavaScript", "JavaScript programming", 18000),
        ],
        "Math": [
            Course("Algebra", "Algebra", 10000),
            Course("Calculus", "Calculus", 20000),
            Course("Statistics", "Statistics", 15000),
            Course("Geometry", "Geometry", 18000),
        ],
        "Physics": [
            Course("Thermodynamics", "Thermodynamics", 18000),
            Course("Optics", "Optics", 22000),
            Course("Quantum Mechanics", "Quantum Mechanics", 25000),
            Course("Nuclear Physics", "Nuclear Physics", 20000),
        ],
        "Chemistry": [
            Course("Organic Chemistry", "Organic Chemistry", 12000),
            Course("Inorganic Chemistry", "Inorganic Chemistry", 22000),
            Course("Physical Chemistry", "Physical Chemistry", 18000),
            Course("Analytical Chemistry", "Analytical Chemistry", 20000),
        ],
        "History": [
            Course("World History", "World History", 12000),
            Course("Ancient History", "Ancient History", 15000),
            Course("Modern History", "Modern History", 18000),
            Course("European History", "European History", 20000),
        ],
        "Art": [
            Course("Drawing", "Drawing", 10000),
            Course("Painting", "Painting", 12000),
            Course("Sculpture", "Sculpture", 15000),
            Course("Photography", "Photography", 18000),
        ],
    }

    for name in teachers_name:
        controller.add_user(
            Teacher(
                name=name,
                email=f"{name}@example.com",
                hashed_password=password_hasher.hash("password"),
            )
        )

    for name in users_name:
        controller.add_user(
            User(
                name=name,
                email=f"{name}@example.com",
                hashed_password=password_hasher.hash("password"),
            )
        )

    for category, courses in courses.items():
        category = CourseCategory(name=category)
        for course in courses:
            category.add_course(course)
        controller.add_category(category)
