__all__ = ["router"]


from .school import router
from .subject_view import router as subject_router

router.include_router(subject_router)
