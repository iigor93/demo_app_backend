from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BannerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
    image: str
    position: int
    name: str | None
    description: str | None
    active: bool


class NewsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
    image: str | None
    position: int
    name: str | None
    description: str | None
    active: bool
