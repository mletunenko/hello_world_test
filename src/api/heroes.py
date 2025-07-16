from fastapi import APIRouter, Depends, HTTPException

from core.enums import ClientErrorMessage
from core.exceptions import ExternalAPIError, HeroAlreadyExists, HeroNotFound
from db.postgres import SessionDep
from schemas.hero import HeroCreate, HeroListParams, HeroOut
from services.heroes import HeroService

router = APIRouter(prefix="/hero", tags=["hero"])


@router.post("", summary="Создать нового героя", response_model=list[HeroOut])
async def add_hero(data: HeroCreate, session: SessionDep) -> list[HeroOut]:
    try:
        created_heroes = await HeroService.create_hero(data.name, session)
        return created_heroes
    except ExternalAPIError:
        raise HTTPException(status_code=502, detail=ClientErrorMessage.EXTERNAL_API_ERROR.value)
    except HeroNotFound:
        raise HTTPException(status_code=404, detail=ClientErrorMessage.HERO_NOT_FOUND_ERROR.value)
    except HeroAlreadyExists:
        raise HTTPException(status_code=409, detail=ClientErrorMessage.HERO_ALREADY_EXISTS_ERROR.value)


@router.get("", summary="Получить список героев", response_model=list[HeroOut])
async def list_heroes(session: SessionDep, query_params: HeroListParams = Depends()) -> list[HeroOut]:
    try:
        heroes = await HeroService.get_heroes_list(session, query_params)
    except HeroNotFound:
        raise HTTPException(status_code=404, detail=ClientErrorMessage.HERO_NOT_FOUND_ERROR.value)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return heroes
