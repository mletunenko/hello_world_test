import asyncio

import uvicorn
from fastapi import APIRouter, FastAPI

from core.config import settings

combined_router = APIRouter(prefix="/api/v1")

app = FastAPI()
app.include_router(combined_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.run.host, port=settings.run.port, reload=True)
