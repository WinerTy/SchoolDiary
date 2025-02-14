from typing import TYPE_CHECKING

from sqladmin import Admin

from core.database.utils import db_helper
from .admin_models import UserAdmin, SchoolAdmin

if TYPE_CHECKING:
    from fastapi import FastAPI


def create_admin_app(app: "FastAPI", authentication_backend) -> None:
    admin = Admin(app, db_helper.engine)

    admin.add_view(UserAdmin)
    admin.add_view(SchoolAdmin)
