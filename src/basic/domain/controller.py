from src.basic.data.repositories import BannerRepository, NewsRepository, WorkoutRepository
from src.basic.domain.schemas import BannerResponse, NewsResponse, WorkoutsResponse


class BannerController:
    def __init__(self, repository: BannerRepository) -> None:
        self.repository = repository

    async def get_banners(self) -> list[BannerResponse]:
        return await self.repository.get_banners()


class NewsController:
    def __init__(self, repository: NewsRepository) -> None:
        self.repository = repository

    async def get_news(self) -> list[NewsResponse]:
        return await self.repository.get_news()


class WorkoutController:
    def __init__(self, repository: WorkoutRepository) -> None:
        self.repository = repository

    async def get_workouts(self) -> WorkoutsResponse:
        return await self.repository.get_workouts()
