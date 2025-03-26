import contextlib

from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminConfig, AdminUser, AuthProvider
from starlette_admin.exceptions import LoginFailed

from api.dependencies.auth import get_users_db, get_user_manager
from core.database.crud.user import UserLogin
from core.database.utils import db_helper

get_users_db_context = contextlib.asynccontextmanager(get_users_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


class AdminAuthProvider(AuthProvider):
    """
    This is only for demo purpose, it's not a better
    way to save and validate user credentials
    """

    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response:
        async with db_helper.session_factory() as session:
            async with get_users_db_context(session=session) as users_db:
                async with get_user_manager_context(users_db=users_db) as user_manager:
                    user = await user_manager.authenticate(
                        credentials=UserLogin(username=username, password=password)
                    )
                    if user:
                        request.session.update({"username": user.email})
                        return response

        raise LoginFailed("Неправильный логин или пароль")

    async def is_authenticated(self, request) -> bool:
        async with db_helper.session_factory() as session:
            async with get_users_db_context(session=session) as users_db:
                user = await users_db.get_by_email(
                    request.session.get("username", None)
                )
                if user and user.is_superuser:
                    request.state.user = user
                    return True
        return False

    def get_admin_config(self, request: Request) -> AdminConfig:
        user = request.state.user  # Retrieve current user
        # Update app title according to current_user
        custom_app_title = "Hello, " + user.email + "!"
        # Update logo url according to current_user
        return AdminConfig(
            app_title=custom_app_title,
        )

    def get_admin_user(self, request: Request) -> AdminUser:
        user = request.state.user  # Retrieve current user
        return AdminUser(username=user.email)

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response
