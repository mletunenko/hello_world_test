from typing import Callable
from unittest.mock import AsyncMock, MagicMock

import pytest

from core.exceptions import ExternalAPIError, HeroAlreadyExists, HeroNotFound
from schemas.hero import HeroCreate
from services.heroes import HeroService
from tests.unit.conftest import make_mock_session

### HeroService.create_hero


@pytest.mark.asyncio
async def test_create_single_hero(
    mock_empty_session: MagicMock, hero_create: HeroCreate, mock_hero_api: Callable
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
    heroes = await HeroService.create_hero(hero_create.name, mock_empty_session)

    assert isinstance(heroes, list)
    assert heroes[0].name == hero_create.name

    assert mock_empty_session.add.call_count == len(heroes)
    mock_empty_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_create_existent_hero(hero_create: HeroCreate, mock_hero_api: Callable) -> None:
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
    session = make_mock_session(scalars_first=hero_create)
    with pytest.raises(HeroAlreadyExists) as exc_info:
        await HeroService.create_hero(hero_create.name, session)

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
    hero_create: HeroCreate, mock_empty_session: AsyncMock, mock_hero_api: Callable
) -> None:
    mock_hero_api(status_code=500)

    with pytest.raises(ExternalAPIError) as exc_info:
        await HeroService.create_hero(hero_create.name, mock_empty_session)

    assert exc_info.type == ExternalAPIError

    mock_empty_session.execute.assert_not_called()
    mock_empty_session.commit.assert_not_called()


@pytest.mark.asyncio
async def test_create_duplicated_heroes(
    hero_create: HeroCreate, mock_empty_session: AsyncMock, mock_hero_api: Callable
) -> None:
    maverick_1 = {
        "id": "1",
        "name": hero_create.name,
        "powerstats": {
            "intelligence": "34",
            "strength": "70",
            "speed": "90",
            "power": "80",
        },
    }
    maverick_2 = {
        "id": "2",
        "name": hero_create.name,
        "powerstats": {
            "intelligence": "34",
            "strength": "70",
            "speed": "90",
            "power": "80",
        },
    }
    data = {"results": [maverick_1, maverick_2]}
    mock_hero_api(status_code=200, json_data=data)

    heroes = await HeroService.create_hero(hero_create.name, mock_empty_session)

    assert len(heroes) == 2
    assert all(hero.name == hero_create.name for hero in heroes)
    assert mock_empty_session.add.call_count == 2


@pytest.mark.asyncio
async def test_create_hero_one_exists_one_new(
    hero_create: HeroCreate, mock_hero_api: Callable, mock_empty_session: AsyncMock
) -> None:
    maverick_1 = {
        "id": "1",
        "name": hero_create.name,
        "powerstats": {
            "intelligence": "34",
            "strength": "70",
            "speed": "90",
            "power": "80",
        },
    }
    maverick_2 = {
        "id": "2",
        "name": hero_create.name,
        "powerstats": {
            "intelligence": "34",
            "strength": "70",
            "speed": "90",
            "power": "80",
        },
    }
    data = {"results": [maverick_1, maverick_2]}
    mock_hero_api(status_code=200, json_data=data)

    existing_result = MagicMock()
    existing_result.scalars.return_value.first.return_value = True  # Существует

    new_result = MagicMock()
    new_result.scalars.return_value.first.return_value = None  # Не существует

    mock_empty_session.execute.side_effect = [existing_result, new_result]

    result = await HeroService.create_hero(hero_create.name, mock_empty_session)

    assert len(result) == 1
    assert result[0].external_id == 2
    assert mock_empty_session.add.call_count == 1


@pytest.mark.asyncio
async def test_create_hero_no_results_key(mock_hero_api: Callable, mock_empty_session: AsyncMock) -> None:
    data = {"some_unexpected_field": []}

    mock_hero_api(status_code=200, json_data=data)

    with pytest.raises(HeroNotFound):
        await HeroService.create_hero("Phantom", mock_empty_session)
