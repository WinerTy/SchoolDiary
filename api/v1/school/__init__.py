__all__ = ["router"]


from .lesson_view import router as lesson_router
from .school import router
from .subject_view import router as subject_router

router.include_router(subject_router)
router.include_router(lesson_router)
