from pathlib import Path
import shutil

from fastapi import HTTPException

from app.pipelines.ingestion_pipeline import IngestionPipeline
from app.pipelines.graph_ingestion_pipeline import GraphIngestionPipeline

from app.repository.repository_service import RepositoryService

from app.services.pinecone_service import PineconeService
from app.graph.graph_service import GraphService

from app.utils.github import extract_repository_name


class IngestionService:

    def __init__(self):

        self.vector_pipeline = IngestionPipeline()

        self.graph_pipeline = GraphIngestionPipeline()

        self.repository_service = RepositoryService()

        self.pinecone_service = PineconeService()

        self.graph_service = GraphService()

    def rollback(
        self,
        user_id: str,
        repository_name: str,
        repository_path: str | None,
    ):

        self.rollback_pinecone(
            user_id=user_id,
            repository_name=repository_name,
        )

        self.rollback_graph(
            user_id=user_id,
            repository_name=repository_name,
        )

        self.rollback_files(
            repository_path=repository_path,
        )

    def rollback_files(
        self,
        repository_path: str | None,
    ):

        if repository_path is None:
            return

        path = Path(repository_path)

        if path.exists():
            shutil.rmtree(path)

    def rollback_pinecone(
        self,
        user_id: str,
        repository_name: str,
    ):

        self.pinecone_service.delete_repository(
            user_id=user_id,
            repository_name=repository_name,
        )

    def rollback_graph(
        self,
        user_id: str,
        repository_name: str,
    ):

        self.graph_service.delete_repository(
            user_id=user_id,
            repository_name=repository_name,
        )

    def ingest(
        self,
        user_id: str,
        repository_url: str,
    ):

        repository_name = extract_repository_name(
            repository_url
        )

        if self.repository_service.exists(
            user_id=user_id,
            repository_name=repository_name,
        ):
            raise HTTPException(
                status_code=409,
                detail="Repository already exists.",
            )

        repository_path = None

        try:

            vector_result = self.vector_pipeline.ingest(
                user_id=user_id,
                repository_url=repository_url,
            )

            repository_path = vector_result["repository_path"]

            self.graph_pipeline.ingest(
                user_id=user_id,
                repository_path=repository_path,
                repository_name=repository_name,
            )

            repository = self.repository_service.create(
                user_id=user_id,
                repository_name=repository_name,
                repository_url=repository_url,
            )

            return {
                "repository_id": repository.id,
                "repository_name": repository.repository_name,
                "documents": vector_result["documents"],
                "chunks": vector_result["chunks"],
                "embeddings": vector_result["embeddings"],
            }

        except Exception:

            self.rollback(
                user_id=user_id,
                repository_name=repository_name,
                repository_path=repository_path,
            )

            raise