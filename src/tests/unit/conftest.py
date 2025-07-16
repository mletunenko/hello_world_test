import uuid
from types import TracebackType
from typing import Any, Callable, Optional, Type
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from models.base import Base
from schemas.hero import HeroCreate, HeroOut


@pytest_asyncio.fixture
def hero_create() -> HeroCreate:
    return HeroCreate(name="Maverick")


@pytest_asyncio.fixture
def hero_out() -> HeroOut:
    return HeroOut(
        id=uuid.uuid4(),
        name="Maverick",
        intelligence=50,
        strength=50,
        speed=50,
        power=50,
        external_id=1,
    )


@pytest_asyncio.fixture
def mock_hero_api(monkeypatch: pytest.MonkeyPatch) -> Callable:
    def factory(
        json_data: dict = None,
        status_code: int = 200,
        raise_for_status: bool = False,
    ) -> None:
        json_data = json_data or {"results": []}

        class MockResponse:
            def __init__(self) -> None:
                self.status_code = status_code

            def json(self) -> dict:
                return json_data

            def raise_for_status(self) -> None:
                if raise_for_status:
                    raise Exception("Mocked HTTP error")

        class MockClient:
            async def __aenter__(self) -> "MockClient":
                return self

            async def __aexit__(
                self,
                exc_type: Optional[Type[BaseException]],
                exc_val: Optional[BaseException],
                exc_tb: Optional[TracebackType],
            ) -> Optional[bool]:
                pass

            async def get(self, *args: Any, **kwargs: Any) -> MockResponse:  # noqa: ANN401
                return MockResponse()

        monkeypatch.setattr("httpx.AsyncClient", lambda: MockClient())

    return factory


# Моки для БД


@pytest.fixture
def mock_empty_session() -> AsyncMock:
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = []
    mock_scalars.first.return_value = None

    mock_result = MagicMock()
    mock_result.scalars.return_value = mock_scalars

    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute.return_value = mock_result
    return mock_session


def make_mock_session(
    *,
    scalars_all: list[Base] = None,
    scalars_first: Optional[Base] = None,
) -> MagicMock:
    """
    Создает мок AsyncSession с гибким заданием результатов.
    Аргументы:
        scalars_all: список, который должен вернуть scalars().all()
        scalars_first: значение, которое должен вернуть scalars().first()
    Возвращает:
        мок AsyncSession с настроенными методами
    """

    mock_scalars = MagicMock()

    if scalars_all is not None:
        mock_scalars.all.return_value = scalars_all
    if scalars_first is not None:
        mock_scalars.first.return_value = scalars_first

    mock_result = MagicMock()
    mock_result.scalars.return_value = mock_scalars

    mock_session = MagicMock(spec=AsyncSession)
    mock_session.execute = AsyncMock(return_value=mock_result)
    return mock_session
