from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.admin import setup_admin
from src.basic.views.router import router
from src.storage import ensure_s3_bucket


@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_s3_bucket()
    yield


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(router)
    setup_admin(app)
    return app


app = create_app()
