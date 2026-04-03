from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.basic.data.models import Banner
from src.basic.domain.schemas import BannerResponse


class BannerRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_banners(self) -> list[BannerResponse]:
        statement = select(Banner).where(Banner.active.is_(True)).order_by(
            desc(Banner.position),
            desc(Banner.id),
        )
        result = await self.session.execute(statement)
        banners = result.scalars().all()
        return [BannerResponse.model_validate(banner) for banner in banners]
