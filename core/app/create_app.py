from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_pagination import add_pagination

from api import router
from core.app.admin.admin_app import create_admin_app
from core.database.utils import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()


def create_application() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        default_response_class=ORJSONResponse,
    )
    admin_app = create_admin_app()
    admin_app.mount_to(app)
    app.include_router(router)
    add_pagination(app)

    return app
