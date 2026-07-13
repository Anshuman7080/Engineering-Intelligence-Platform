from functools import lru_cache

from app.pipelines.query_pipeline import QueryPipeline
from app.pipelines.ingestion_pipeline import IngestionPipeline


@lru_cache
def get_query_pipeline():
    return QueryPipeline()


@lru_cache
def get_ingestion_pipeline():
    return IngestionPipeline()