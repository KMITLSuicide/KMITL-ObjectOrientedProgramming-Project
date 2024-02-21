from fastapi import APIRouter, Body

router = APIRouter()

@router.get("/example/")
async def get_example():
    return "hi"

