from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.basic.data.models import Banner, News
from src.basic.domain.schemas import BannerResponse, NewsResponse


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


class NewsRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_news(self) -> list[NewsResponse]:
        statement = (
            select(News)
            .where(News.active.is_(True))
            .order_by(
                desc(News.position),
                desc(News.id),
            )
            .limit(10)
        )
        result = await self.session.execute(statement)
        news = result.scalars().all()
        return [NewsResponse.model_validate(item) for item in news]
