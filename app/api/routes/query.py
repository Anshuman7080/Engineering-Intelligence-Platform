from fastapi import APIRouter,Depends

from app.api.schemas.query import QueryRequest
from app.pipelines.query_pipeline import QueryPipeline
from app.api.dependencies import get_query_pipeline

router = APIRouter()




@router.post("/")
async def ask_question(
    request: QueryRequest,
    pipeline:QueryPipeline=Depends(get_query_pipeline),
):

    result = await pipeline.ask(
        query=request.question,
        repository_name=request.repository_name,
        conversation_id=request.conversation_id,
        top_k=request.top_k,
    )

    return result