from typing import Callable
from unittest.mock import AsyncMock, MagicMock

import pytest

from core.exceptions import ExternalAPIError, HeroAlreadyExists, HeroNotFound
from schemas.hero import HeroCreate
from services.heroes import HeroService
from tests.unit.conftest import make_mock_session


@pytest.mark.asyncio
async def test_create_single_hero(
    mock_empty_session: MagicMock, unique_hero: HeroCreate, mock_hero_api: Callable
) -> None:
    data = {
        "results": [
            {
                "id": "1",
                "name": "Maverick",
                "powerstats": {
                    "intelligence": "85",
                    "strength": "70",
                    "speed": "90",
                    "power": "80",
                },
            }
        ]
    }
    mock_hero_api(json_data=data)
    heroes = await HeroService.create_hero(unique_hero.name, mock_empty_session)

    assert isinstance(heroes, list)
    assert heroes[0].name == unique_hero.name

    assert mock_empty_session.add.call_count == len(heroes)
    mock_empty_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_create_existent_hero(unique_hero: HeroCreate, mock_hero_api: Callable) -> None:
    data = {
        "results": [
            {
                "id": "1",
                "name": "Maverick",
                "powerstats": {
                    "intelligence": "85",
                    "strength": "70",
                    "speed": "90",
                    "power": "80",
                },
            }
        ]
    }
    mock_hero_api(json_data=data)
    session = make_mock_session(scalars_first=unique_hero)
    with pytest.raises(HeroAlreadyExists) as exc_info:
        await HeroService.create_hero(unique_hero.name, session)

    assert exc_info.type == HeroAlreadyExists

    session.execute.assert_called_once()
    session.commit.assert_not_called()


@pytest.mark.asyncio
async def test_create_not_found_hero(mock_empty_session: AsyncMock, mock_hero_api: Callable) -> None:
    mock_hero_api(json_data={"results": []})

    invalid_name = "qwertyuiop"
    with pytest.raises(HeroNotFound) as exc_info:
        await HeroService.create_hero(invalid_name, mock_empty_session)

    assert exc_info.type == HeroNotFound

    mock_empty_session.execute.assert_not_called()
    mock_empty_session.commit.assert_not_called()


@pytest.mark.asyncio
async def test_create_api_error_hero(
    unique_hero: HeroCreate, mock_empty_session: AsyncMock, mock_hero_api: Callable
) -> None:
    mock_hero_api(status_code=500)

    with pytest.raises(ExternalAPIError) as exc_info:
        await HeroService.create_hero(unique_hero.name, mock_empty_session)

    assert exc_info.type == ExternalAPIError

    mock_empty_session.execute.assert_not_called()
    mock_empty_session.commit.assert_not_called()
