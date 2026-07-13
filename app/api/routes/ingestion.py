from fastapi import APIRouter,Depends

from app.api.schemas.ingestion import IngestionRequest
from app.pipelines.ingestion_pipeline import IngestionPipeline
from app.api.dependencies import get_ingestion_pipeline

router = APIRouter()




@router.post("/")
async def ingest_repository(
    request: IngestionRequest,
    pipeline:IngestionPipeline=Depends(get_ingestion_pipeline),
):

    result = pipeline.ingest(
        repository_url=request.repository_url,
    )

    return result