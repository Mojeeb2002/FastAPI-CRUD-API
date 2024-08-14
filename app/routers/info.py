from fastapi import APIRouter

router = APIRouter(
    prefix="/info",
    tags=["info"],
)

@router.get("/author")
def information():
    return {
        "Author": "Mojeeb Suliman Abdallah Dafallah",
        "Date" : "14-08-2024",
    }

