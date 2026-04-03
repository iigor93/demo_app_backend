from src.basic.data.repositories import BannerRepository
from src.basic.domain.schemas import BannerResponse


class BannerController:
    def __init__(self, repository: BannerRepository) -> None:
        self.repository = repository

    async def get_banners(self) -> list[BannerResponse]:
        return await self.repository.get_banners()
