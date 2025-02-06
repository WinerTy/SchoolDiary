from fastapi import APIRouter

from api.dependencies.auth import authentication_backend
from .fastapi_users import fastapi_users

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


router.include_router(
    router=fastapi_users.get_auth_router(
        authentication_backend,
    )
)
