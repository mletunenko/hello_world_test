from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class HeroModel(Base):
    __tablename__ = "heroes"
    external_id: Mapped[int] = mapped_column(nullable=True, unique=True)
    name: Mapped[str] = mapped_column(default="")
    intelligence: Mapped[int] = mapped_column(nullable=True)
    strength: Mapped[int] = mapped_column(nullable=True)
    speed: Mapped[int] = mapped_column(nullable=True)
    power: Mapped[int] = mapped_column(nullable=True)
