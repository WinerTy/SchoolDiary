from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api import router
from core.app.admin.admin_app import create_admin_app
from core.app.admin.auth import get_admin_auth
from core.database.utils import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    authentication_backend = await get_admin_auth()
    create_admin_app(app, authentication_backend)
    yield
    await db_helper.dispose()


def create_application() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        default_response_class=ORJSONResponse,
    )

    app.include_router(router)

    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    return app
