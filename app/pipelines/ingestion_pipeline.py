from pathlib import Path
from app.ingestion.git_service import GitService
from app.ingestion.loader import RepositoryLoader
from app.ingestion.chunker import DocumentChunker
from app.services.embedding_service import EmbeddingService
from app.services.pinecone_service import PineconeService
from app.core.logger import logger
from app.ingestion.commit_loader import CommitLoader
from app.ingestion.pr_loader import PullRequestLoader

class IngestionPipeline:

    def __init__(self):

        self.git_service = GitService()

        self.loader = RepositoryLoader()

        self.chunker = DocumentChunker()

        self.embedding_service = EmbeddingService()

        self.pinecone_service = PineconeService()
        
        self.commit_loader=CommitLoader()

        self.pr_loader = PullRequestLoader()

    def ingest(
    self,
    repository_url: str,
    ): 
        repository_name = (
            repository_url
            .rstrip("/")
            .split("/")[-1]
            .replace(".git", "")
        )

        destination = f"data/repositories/{repository_name}"

        repository_path = self.git_service.clone_repository(
            repository_url=repository_url,
            destination=destination,
        )   

        file_documents = self.loader.load(repository_path)

        commit_documents = self.commit_loader.load(
            repository_path
        )

        pr_documents = self.pr_loader.load(
            repository_url
        )

        documents = (
            file_documents
            + commit_documents
            + pr_documents
        )

        

        chunks = self.chunker.split_documents(documents)

        embeddings = self.embedding_service.embed_documents(
            chunks
        )

        self.pinecone_service.upsert_documents(
            documents=chunks,
            embeddings=embeddings,
            repository_name=repository_name,
        )

        return {
        "repository": repository_name,
        "documents": len(documents),
        "chunks": len(chunks),
        "embeddings": len(embeddings),
        }
        
