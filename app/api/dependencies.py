from functools import lru_cache


from app.pipelines.ingestion_pipeline import IngestionPipeline



@lru_cache
def get_ingestion_pipeline():
    return IngestionPipeline()