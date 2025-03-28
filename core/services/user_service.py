from core.database import User
from core.database.crud import UserRepository
from core.database.crud.user import UserRead, UserUpdate, UserCreate
from core.services.base_services import BaseService


class UserService(BaseService[User, UserCreate, UserUpdate, UserRead]):
    def __init__(self, user_repo: UserRepository):
        super().__init__(repositories={"user": user_repo})

    async def update_user(self, user_id: int, update_data: UserUpdate) -> User:
        user_repo = self.get_repo("user")
        return await user_repo.update(user_id, update_data)
