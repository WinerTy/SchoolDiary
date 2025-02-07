from fastapi import APIRouter

from .v1.application import router as application_router
from .v1.auth import router as auth_router

router = APIRouter(
    prefix="/api",
)
router.include_router(auth_router)
router.include_router(application_router)
