from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from fastapi.security import OAuth2PasswordRequestForm
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from core.config import config
from core.database.utils import db_helper

if TYPE_CHECKING:
    pass


class AdminAuth(AuthenticationBackend):
    def __init__(self, secret: str):
        super().__init__(secret)

    @asynccontextmanager
    async def get_session(self) -> AsyncSession:
        session_gen = db_helper.session_getter()
        session = await session_gen.__anext__()  # Получаем сессию из генератора
        try:
            yield session  # Передаем сессию в блок with
        finally:
            await session.close()  # Закрываем сессию
            try:
                await session_gen.__anext__()  # Завершаем генератор
            except StopAsyncIteration:
                pass  # Генератор завершился, это нормально

    async def login(self, request: Request) -> bool:  # WARNING Maybe not optimal
        form = await request.form()
        username, password = form["username"], form["password"]
        data: OAuth2PasswordRequestForm = OAuth2PasswordRequestForm(
            username=username, password=password
        )
        # async with self.get_session() as session:
        #     user_db = User.get_db(session=session)
        #     manager = UserManager(user_db)
        #     result = await manager.authenticate(data)

        # Validate username/password credentials
        # And update session
        request.session.update({"token": "..."})

        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        # Check the token in depth
        return True


async def get_admin_auth() -> AdminAuth:
    return AdminAuth(secret=config.auth.secret)
