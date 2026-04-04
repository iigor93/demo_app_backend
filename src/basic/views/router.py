from fastapi import APIRouter

from src.basic.domain.schemas import BannerResponse, NewsResponse
from src.session import BannerControllerDep, NewsControllerDep


router = APIRouter(prefix="/api/v1")


@router.get("/")
async def healthcheck() -> str:
    return "OK"


@router.get("/banners", response_model=list[BannerResponse])
async def get_banners(
    controller: BannerControllerDep,
) -> list[BannerResponse]:
    return await controller.get_banners()


@router.get("/news", response_model=list[NewsResponse])
async def get_news(
    controller: NewsControllerDep,
) -> list[NewsResponse]:
    return await controller.get_news()
