from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from api.dependencies.auth import authentication_backend
from core.database import User
from core.database.crud.base.repository import BaseRepository
from core.database.schemas.user import UserRead, UserCreate
from core.database.utils import db_helper
from .fastapi_users import fastapi_users


class UserRepository(BaseRepository[User, UserCreate, UserRead, UserRead]):
    def __init__(self, session):
        super().__init__(User, session)


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


router.include_router(
    router=fastapi_users.get_auth_router(
        authentication_backend,
    )
)
router.include_router(
    router=fastapi_users.get_register_router(
        UserRead,
        UserCreate,
    ),
)


@router.get("/user/{id}", response_model=UserRead)
async def get_user(
    id: int, session: Annotated["AsyncSession", Depends(db_helper.session_getter)]
):
    repo = UserRepository(session)
    item = await repo.get_by_id(id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
