from app.ingestion.git_service import GitService
from app.ingestion.loader import RepositoryLoader
from app.ingestion.chunker import DocumentChunker
from app.services.embedding_service import EmbeddingService
from app.services.pinecone_service import PineconeService
from app.ingestion.commit_loader import CommitLoader
from app.ingestion.pr_loader import PullRequestLoader
from app.utils.github import extract_repository_name


class IngestionPipeline:

    def __init__(self):

        self.git_service = GitService()
        self.loader = RepositoryLoader()
        self.chunker = DocumentChunker()
        self.embedding_service = EmbeddingService()
        self.pinecone_service = PineconeService()
        self.commit_loader = CommitLoader()
        self.pr_loader = PullRequestLoader()

    def ingest(
        self,
        user_id: str,
        repository_url: str,
    ):

        repository_name = extract_repository_name(
            repository_url
        )

        destination = (
            "data/repositories/"
            + repository_name.replace("/", "__")
        )

        repository_path = self.git_service.clone_repository(
            repository_url=repository_url,
            destination=destination,
        )

        file_documents = self.loader.load(
            repository_path
        )

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

        chunks = self.chunker.split_documents(
            documents
        )

        embeddings = self.embedding_service.embed_documents(
            chunks
        )

        self.pinecone_service.upsert_documents(
            documents=chunks,
            embeddings=embeddings,
            user_id=user_id,
            repository_name=repository_name,
        )

        return {
            "repository": repository_name,
            "repository_path": repository_path,
            "documents": len(documents),
            "chunks": len(chunks),
            "embeddings": len(embeddings),
        }