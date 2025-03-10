from fastapi import APIRouter

router: APIRouter = APIRouter(
    prefix="/lesson",
    tags=["Lesson"],
)
