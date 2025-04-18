from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from core.database import User, Grade, SchoolSubject, Lesson
from core.database.crud import UserRepository
from core.database.crud.user import UserRead, UserUpdate, UserCreate
from core.services.base_services import BaseService


class UserService(BaseService[User, UserCreate, UserUpdate, UserRead]):
    def __init__(self, user_repo: UserRepository):
        super().__init__(repositories={"user": user_repo})

    async def update_user(self, user_id: int, update_data: UserUpdate) -> User:
        user_repo = self.get_repo("user")
        return await user_repo.update(user_id, update_data)

    async def get_grade_with_filter(
        self, user: User, subjects: Optional[List[str]] = None
    ):
        stmt = select(Grade).where(Grade.user_id == user.id)

        if subjects:
            stmt = stmt.join(Grade.lesson).join(Lesson.school_subjects)
            stmt = stmt.where(SchoolSubject.subject_name.in_(subjects))

        stmt = stmt.options(
            joinedload(Grade.lesson).joinedload(Lesson.school_subjects),
            joinedload(Grade.user),
        )
        user_repo = self.get_repo("user")
        result = await user_repo.db.execute(stmt)

        return result.unique().scalars().all()
