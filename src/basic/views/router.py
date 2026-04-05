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


@router.get("/coordinates", response_model=list)
async def get_coordinates() -> list:
    return [
        {
            "lat": 55.7558,
            "lon": 37.6176,
            "name": "Красная площадь",
            "description": "Тестовая точка в центре Москвы.",
        },
        {
            "lat": 55.9167,
            "lon": 37.8167,
            "name": "Мытищи",
            "description": "Тестовая точка в Московской области.",
        },
    ]
