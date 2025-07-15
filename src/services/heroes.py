from operator import and_

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.exceptions import ExternalAPIError, HeroAlreadyExists, HeroNotFound
from core.logger import logger
from models import HeroModel
from schemas.hero import HeroOut


async def create_hero(name: str, session: AsyncSession) -> list[HeroOut]:
    async with httpx.AsyncClient() as client:
        url = f"{settings.hero_api.base_url}/{settings.hero_api.token}/search/{name}"
        response = await client.get(url)

    if response.status_code != 200:
        raise ExternalAPIError

    data = response.json()
    results = data.get("results", [])

    matched = [h for h in results if h["name"].lower() == name.lower()]
    if not matched:
        raise HeroNotFound

    created = []
    for h in matched:
        external_id = int(h["id"])

        result = await session.execute(
            select(HeroModel).where(and_(HeroModel.name == h["name"], HeroModel.external_id == external_id))
        )
        exists = result.scalar_one_or_none()
        if exists:
            continue

        try:
            stats = h["powerstats"]
            hero = HeroModel(
                name=h["name"],
                external_id=external_id,
                intelligence=None if stats["intelligence"] == "null" else int(stats["intelligence"]),
                strength=None if stats["intelligence"] == "null" else int(stats["intelligence"]),
                speed=None if stats["intelligence"] == "null" else int(stats["intelligence"]),
                power=None if stats["intelligence"] == "null" else int(stats["intelligence"]),
            )
        except (KeyError, ValueError) as exc:
            logger.exception(exc)
            continue

        session.add(hero)
        created.append(hero)

    if not created:
        raise HeroAlreadyExists(f"{name} уже есть в базе")

    await session.commit()
    for hero in created:
        await session.refresh(hero)

    return created
