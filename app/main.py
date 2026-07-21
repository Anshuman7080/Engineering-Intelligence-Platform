from fastapi import FastAPI

from app.core.settings import settings
from app.core.logger import logger

from app.api.routes.health import router as health_router
from app.api.routes.ingestion import router as ingestion_router
from app.database.init_db import init_db
from app.api.routes.chat import (
    router as chat_router,
)
from app.api.routes.auth import (
    router as auth_router
)



init_db()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)


logger.info("Application started")



app.include_router(
    health_router,
    prefix="/health",
    tags=["Health"],
)

app.include_router(
    ingestion_router,
    prefix="/ingest",
    tags=["Ingestion"],
)

app.include_router(
    chat_router,
    prefix="/chat",
    tags=["Chat"],
)

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"],
)


@app.get("/")
async def root():
    return {
        "message": settings.APP_NAME
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }