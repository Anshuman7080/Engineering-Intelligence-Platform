from langchain_core.documents import Document
from pinecone import Pinecone

from app.core.logger import logger
from app.core.settings import settings


class PineconeService:

    def __init__(self):

        logger.info("Initializing Pinecone client.")

        self.pc = Pinecone(
            api_key=settings.PINECONE_API_KEY
        )

        self.index = self.pc.Index(
            settings.PINECONE_INDEX_NAME
        )

        logger.info(
            f"Connected to Pinecone index: {settings.PINECONE_INDEX_NAME}"
        )

    def upsert_documents(
        self,
        documents: list[Document],
        embeddings: list[list[float]],
        repository_name: str,
        batch_size: int = 100,
    ):

        logger.info(
            f"Uploading {len(documents)} documents to Pinecone."
        )

        vectors = []

        for index, (document, embedding) in enumerate(
            zip(documents, embeddings)
        ):

            vector = {
                "id": f"{repository_name}_{index}",
                "values": embedding,
                "metadata": {
                    "repository": repository_name,
                    "source": document.metadata.get("source", ""),
                    "chunk_index": index,
                    "text": document.page_content,
                },
            }

            vectors.append(vector)

        for i in range(0, len(vectors), batch_size):

            batch = vectors[i:i + batch_size]

            self.index.upsert(
                vectors=batch
            )

            logger.info(
                f"Uploaded batch {(i // batch_size) + 1}"
            )

        logger.info(
            f"Successfully uploaded {len(vectors)} vectors."
        )

    def similarity_search(
        self,
        embedding: list[float],
        top_k: int = 5,
        repository_name: str | None = None,
    ):

        logger.info("Searching Pinecone.")

        filter_dict = None

        if repository_name:

            filter_dict = {
                "repository": {
                    "$eq": repository_name
                }
            }

        results = self.index.query(
            vector=embedding,
            top_k=top_k,
            include_metadata=True,
            filter=filter_dict,
        )
        # results = self.index.query(
        #     vector=embedding,
        #     top_k=top_k,
        #     include_metadata=True,
            
        # )

        logger.info(
            f"Retrieved {len(results.matches)} matches."
        )

        return results.matches

    def delete_repository(
        self,
        repository_name: str,
    ):

        logger.info(
            f"Deleting repository: {repository_name}"
        )

        self.index.delete(
            filter={
                "repository": {
                    "$eq": repository_name
                }
            }
        )

        logger.info("Repository deleted successfully.")