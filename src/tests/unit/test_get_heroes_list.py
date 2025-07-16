import pytest

from core.exceptions import HeroNotFound
from schemas.hero import HeroListParams, HeroOut
from services.heroes import HeroService
from tests.unit.conftest import make_mock_session

### HeroService.list_heroes


@pytest.mark.asyncio
async def test_get_heroes_list_returns_heroes(hero_out: HeroOut) -> None:
    session = make_mock_session(scalars_all=[hero_out])
    params = HeroListParams(name=hero_out.name)

    result = await HeroService.get_heroes_list(session, params)

    assert isinstance(result, list)
    assert result[0].name == hero_out.name
    session.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_heroes_list_no_results() -> None:
    session = make_mock_session(scalars_all=[])
    params = HeroListParams(name="NotExist")

    with pytest.raises(HeroNotFound):
        await HeroService.get_heroes_list(session, params)

    session.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_heroes_list_with_numeric_filters(hero_out: HeroOut) -> None:
    session = make_mock_session(scalars_all=[hero_out])
    params = HeroListParams(
        strength_gte=50,
        intelligence_eq=hero_out.intelligence,
    )

    result = await HeroService.get_heroes_list(session, params)

    assert len(result) == 1
    assert result[0].name == hero_out.name
    session.execute.assert_called_once()
