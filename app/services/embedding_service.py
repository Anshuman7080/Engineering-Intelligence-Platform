from sentence_transformers import SentenceTransformer
from langchain_core.documents import Document

from app.core.settings import settings
from app.core.logger import logger


class EmbeddingService:

    def __init__(self):

        logger.info(
            f"Loading embedding model: {settings.EMBEDDING_MODEL}"
        )

        self.model = SentenceTransformer(
            settings.EMBEDDING_MODEL
        )

        logger.info("Embedding model loaded successfully.")

    def embed_documents(
        self,
        documents: list[Document]
    ) -> list[list[float]]:

        logger.info(
            f"Generating embeddings for {len(documents)} documents."
        )

        texts = [
            document.page_content
            for document in documents
        ]

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True
        )

        logger.info("Document embeddings generated successfully.")

        return embeddings.tolist()

    def embed_query(
        self,
        query: str
    ) -> list[float]:

        logger.info("Generating query embedding.")

        embedding = self.model.encode(
            query,
            normalize_embeddings=True
        )

        return embedding.tolist()