from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi_users import FastAPIUsers
from starlette import status

from api.dependencies.auth import authentication_backend
from api.dependencies.auth import get_user_manager
from api.dependencies.repository import get_school_repository
from api.dependencies.repository.get_repository import get_grade_repository
from core.database import User
from core.database.crud import SchoolRepository
from core.database.crud.grade import GradeRepository
from core.database.models.choices import ChoicesRole

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [authentication_backend],
)


current_active_user = fastapi_users.current_user(active=True)
current_active_superuser = fastapi_users.current_user(active=True, superuser=True)

current_user = Annotated[User, Depends(current_active_user)]


async def current_active_student_user(
    user: current_user,
) -> User:
    if user.role != ChoicesRole.platform_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have the required role",
        )
    return user


async def current_active_teacher_or_admin_in_school(
    school_id: int,
    user: User = Depends(current_active_user),
    school_repo: SchoolRepository = Depends(get_school_repository),
) -> User:
    """
    Проверяет, является ли пользователь учителем или администратором в указанной школе.

    Args:
        school_id: ID школы для проверки
        user: Текущий авторизованный пользователь
        school_repo: Репозиторий для работы со школами

    Returns:
        User: Объект пользователя, если проверка пройдена

    Raises:
        HTTPException: 403 если пользователь не имеет нужной роли или доступа
        HTTPException: 404 если школа не найдена
    """
    # Быстрая проверка роли сначала
    if user.role not in {ChoicesRole.teacher, ChoicesRole.platform_admin}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User role not allowed",
        )

    # Получаем школу или 404
    school = await school_repo.get_school_or_404(school_id)

    # Проверяем привилегии platform_admin (если есть доступ ко всем школам)
    if user.role == ChoicesRole.platform_admin:
        return user

    # Проверяем, является ли пользователь директором или учителем школы
    is_director = user.id == school.director_id
    is_teacher = any(t.id == user.id for t in school.teachers)

    if not (is_director or is_teacher):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not associated with this school",
        )

    return user


async def current_teacher_for_lesson(
    user: current_user,
    grade_id: int,
    grade_repo: Annotated["GradeRepository", Depends(get_grade_repository)],
) -> User:
    grade = await grade_repo.get_by_id(grade_id)
    if grade.lesson.teacher != user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="We are not teacher for this lesson",
        )
    return user
