from datetime import datetime

from pydantic import UUID4, BaseModel, Field

from models import HeroModel


class HeroCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class HeroOut(BaseModel):
    id: UUID4
    created_at: datetime | None = None
    name: str = ""
    intelligence: int | None = None
    strength: int | None = None
    speed: int | None = None
    power: int | None = None
    external_id: int


class HeroListParams(BaseModel):
    name: str | None = None

    intelligence_gte: int | None = None
    intelligence_lte: int | None = None
    intelligence_eq: int | None = None

    strength_gte: int | None = None
    strength_lte: int | None = None
    strength_eq: int | None = None

    speed_gte: int | None = None
    speed_lte: int | None = None
    speed_eq: int | None = None

    power_gte: int | None = None
    power_lte: int | None = None
    power_eq: int | None = None

    def build_filters(self) -> list:
        filters = []

        if self.name:
            filters.append(HeroModel.name == self.name)

        if self.intelligence_gte:
            filters.append(HeroModel.intelligence >= self.intelligence_gte)
        if self.intelligence_lte:
            filters.append(HeroModel.intelligence <= self.intelligence_lte)
        if self.intelligence_eq:
            filters.append(HeroModel.intelligence == self.intelligence_eq)

        if self.strength_gte:
            filters.append(HeroModel.strength >= self.strength_gte)
        if self.strength_lte:
            filters.append(HeroModel.strength <= self.strength_lte)
        if self.strength_eq:
            filters.append(HeroModel.strength == self.strength_eq)

        if self.speed_gte:
            filters.append(HeroModel.speed >= self.speed_gte)
        if self.speed_lte:
            filters.append(HeroModel.speed <= self.speed_lte)
        if self.speed_eq:
            filters.append(HeroModel.speed == self.speed_eq)

        if self.power_gte:
            filters.append(HeroModel.power >= self.power_gte)
        if self.power_lte:
            filters.append(HeroModel.power <= self.power_lte)
        if self.power_eq:
            filters.append(HeroModel.power == self.power_eq)

        return filters
