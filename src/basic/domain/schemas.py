from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, model_validator


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


class WorkoutItem(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str = Field(min_length=1)
    alias: str = Field(min_length=1, pattern=r"^[a-z0-9_]+$")
    exercises: list[Annotated[str, Field(min_length=1)]] = Field(min_length=1)


class WorkoutsResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    workouts: list[WorkoutItem]

    @model_validator(mode="after")
    def validate_unique_aliases(self) -> "WorkoutsResponse":
        aliases = [workout.alias for workout in self.workouts]
        if len(aliases) != len(set(aliases)):
            raise ValueError("workout aliases must be unique")
        return self
