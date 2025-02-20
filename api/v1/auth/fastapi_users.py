from fastapi import Depends, HTTPException
from fastapi_users import FastAPIUsers
from starlette import status

from api.dependencies.auth import authentication_backend
from api.dependencies.auth import get_user_manager
from core.database import User
from core.database.models.choices import ChoicesRole

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [authentication_backend],
)


current_active_user = fastapi_users.current_user(active=True)
current_active_superuser = fastapi_users.current_user(active=True, superuser=True)


async def current_active_student_user(
    user: User = Depends(current_active_user),
) -> User:
    if user.role != ChoicesRole.platform_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have the required role",
        )
    return user


async def current_active_teacher_user_or_admin_user(
    user: User = Depends(current_active_user),
) -> User:
    if user.role != ChoicesRole.teacher and user.role != ChoicesRole.platform_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have the required role",
        )
    return user
