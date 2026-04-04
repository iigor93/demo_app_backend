from fastapi import APIRouter

from src.basic.domain.schemas import BannerResponse
from src.session import BannerControllerDep


router = APIRouter(prefix="/api/v1")


@router.get("/")
async def healthcheck() -> str:
    return "OK"


@router.get("/banners", response_model=list[BannerResponse])
async def get_banners(
    controller: BannerControllerDep,
) -> list[BannerResponse]:
    return await controller.get_banners()
