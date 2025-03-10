from fastapi import APIRouter

from .v1.application import router as application_router
from .v1.auth import router as auth_router
from .v1.school import router as school_router
from .v1.users.users import router as users_router
from .v1.lesson import router as lesson_router
router = APIRouter(
    prefix="/api",
)
router.include_router(auth_router)
router.include_router(application_router)

router.include_router(school_router)
router.include_router(users_router)
router.include_router(lesson_router)