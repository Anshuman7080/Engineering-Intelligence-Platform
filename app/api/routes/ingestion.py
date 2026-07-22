from fastapi import APIRouter,Depends

from app.api.schemas.ingestion import IngestionRequest
from app.pipelines.ingestion_pipeline import IngestionPipeline
from app.api.dependencies.ingestion import get_ingestion_service
from app.pipelines.ingestion_service import IngestionService
from app.api.dependencies.auth import get_current_user

router = APIRouter()


@router.post("/")
async def ingest_repository(
    request: IngestionRequest,
    current_user=Depends(get_current_user),
    pipeline:IngestionService=Depends(get_ingestion_service),
):

    result = pipeline.ingest(
        user_id=current_user["id"],
        repository_url=request.repository_url,
    )

    return result