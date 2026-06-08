from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.basic.domain.controller import BannerController, NewsController, WorkoutController
from src.config import settings
from src.basic.data.repositories import BannerRepository, NewsRepository, WorkoutRepository

engine: AsyncEngine = create_async_engine(settings.async_database_url)
SessionLocal = async_sessionmaker[AsyncSession](
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as db:
        yield db


DBSessionDep = Annotated[AsyncSession, Depends(get_db)]


def banner_repository_factory(
    db: DBSessionDep,
) -> BannerRepository:
    return BannerRepository(db)


BannerRepositoryDep = Annotated[BannerRepository, Depends(banner_repository_factory)]


def banner_controller_factory(
    banner_repository: BannerRepositoryDep,
) -> BannerController:
    return BannerController(repository=banner_repository)


BannerControllerDep = Annotated[BannerController, Depends(banner_controller_factory)]


def news_repository_factory(
    db: DBSessionDep,
) -> NewsRepository:
    return NewsRepository(db)


NewsRepositoryDep = Annotated[NewsRepository, Depends(news_repository_factory)]


def news_controller_factory(
    news_repository: NewsRepositoryDep,
) -> NewsController:
    return NewsController(repository=news_repository)


NewsControllerDep = Annotated[NewsController, Depends(news_controller_factory)]


def workout_repository_factory(
    db: DBSessionDep,
) -> WorkoutRepository:
    return WorkoutRepository(db)


WorkoutRepositoryDep = Annotated[
    WorkoutRepository,
    Depends(workout_repository_factory),
]


def workout_controller_factory(
    workout_repository: WorkoutRepositoryDep,
) -> WorkoutController:
    return WorkoutController(repository=workout_repository)


WorkoutControllerDep = Annotated[
    WorkoutController,
    Depends(workout_controller_factory),
]
