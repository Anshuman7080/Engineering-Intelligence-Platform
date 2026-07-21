from functools import lru_cache


from app.pipelines.ingestion_service import IngestionService



@lru_cache
def get_ingestion_service():
    return IngestionService()