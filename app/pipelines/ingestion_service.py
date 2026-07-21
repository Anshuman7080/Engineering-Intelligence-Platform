from app.pipelines.ingestion_pipeline import IngestionPipeline
from app.pipelines.graph_ingestion_pipeline import GraphIngestionPipeline


class IngestionService:

    def __init__(self):

        self.vector_pipeline = IngestionPipeline()
        self.graph_pipeline = GraphIngestionPipeline()

    def ingest(
        self,
        repository_url: str,
    ):

        vector_result = self.vector_pipeline.ingest(
            repository_url
        )

        self.graph_pipeline.ingest(
            repository_path=vector_result["repository_path"],
            repository_name=vector_result["repository"],
        )

        return {
            "repository": vector_result["repository"],
            "documents": vector_result["documents"],
            "chunks": vector_result["chunks"],
            "embeddings": vector_result["embeddings"],
            "graph": "completed",
        }