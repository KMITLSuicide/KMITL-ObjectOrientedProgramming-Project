from fastapi import APIRouter

router = APIRouter()

@router.get("/example/")
async def get_example():
    return "hi"

