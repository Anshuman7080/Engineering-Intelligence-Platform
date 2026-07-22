from fastapi import APIRouter, Depends
from fastapi.concurrency import run_in_threadpool

from app.api.schemas.ingestion import IngestionRequest
from app.api.dependencies.ingestion import get_ingestion_service
from app.pipelines.ingestion_service import IngestionService
from app.api.dependencies.auth import get_current_user

router = APIRouter()


@router.post("/")
async def ingest_repository(
    request: IngestionRequest,
    current_user=Depends(get_current_user),
    pipeline: IngestionService = Depends(get_ingestion_service),
):

    result = await run_in_threadpool(
        pipeline.ingest,
        current_user.id,
        request.repository_url,
    )

    return result