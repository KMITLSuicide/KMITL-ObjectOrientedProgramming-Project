from fastapi import APIRouter, Body
from backend.definitions.course import *
from backend.controller_instance import controller

router = APIRouter()

@router.get("/example/")
async def get_example():
    return "hi"

# @router.post("/todo", tags=["Todos"])
# async def add_todo(todo: dict) -> dict:
#     todos.append(todo)
#     return {
#         "data": "A Todo is Added!"
#     }