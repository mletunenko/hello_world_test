from fastapi import APIRouter, HTTPException

from core.enums import ClientErrorMessage
from core.exceptions import ExternalAPIError, HeroAlreadyExists, HeroNotFound
from db.postgres import SessionDep
from schemas.hero import HeroCreate, HeroOut
from services.heroes import create_hero

router = APIRouter(prefix="/hero", tags=["hero"])


@router.post("", summary="Создать нового героя", response_model=list[HeroOut])
async def add_hero(data: HeroCreate, session: SessionDep) -> list[HeroOut]:
    try:
        created_heroes = await create_hero(data.name, session)
        return created_heroes
    except ExternalAPIError:
        raise HTTPException(status_code=502, detail=ClientErrorMessage.EXTERNAL_API_ERROR.value)
    except HeroNotFound:
        raise HTTPException(status_code=404, detail=ClientErrorMessage.HERO_NOT_FOUND_ERROR.value)
    except HeroAlreadyExists:
        raise HTTPException(status_code=409, detail=ClientErrorMessage.HERO_ALREADY_EXISTS_ERROR.value)
