from fastapi import APIRouter
import subprocess
import datetime

router = APIRouter()


@router.get("/info/")
async def get_info():
    current_time = datetime.datetime.now()
    commit_sha = subprocess.getoutput("git rev-parse --short HEAD")
    commit_time = subprocess.getoutput('git show -s --format="%cd" --date=iso')
    return {
        "current": {"time": current_time},
        "commit": {"sha": commit_sha, "time": commit_time},
    }
