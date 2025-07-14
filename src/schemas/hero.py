from datetime import datetime

from pydantic import UUID4, BaseModel


class HeroCreate(BaseModel):
    name: str


class HeroInDB(BaseModel):
    name: str
    intelligence: int
    strength: int
    speed: int
    power: int


class HeroOut(BaseModel):
    id: UUID4
    created_at: datetime | None = None
    name: str
    intelligence: int
    strength: int
    speed: int
    power: int
