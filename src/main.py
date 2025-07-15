import uvicorn
from fastapi import APIRouter, FastAPI

from api.heroes import router as heroes_router
from core.config import settings

combined_router = APIRouter(prefix="/api/v1")
combined_router.include_router(heroes_router)

app = FastAPI()
app.include_router(combined_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.run.host, port=settings.run.port, reload=True)
