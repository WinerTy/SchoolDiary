from fastapi_users import FastAPIUsers

from api.dependencies.auth import authentication_backend
from api.dependencies.auth import get_user_manager
from core.database import User

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [authentication_backend],
)
