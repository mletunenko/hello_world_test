from datetime import datetime

from pydantic import UUID4, BaseModel, Field


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
