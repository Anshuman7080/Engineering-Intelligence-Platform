# from sentence_transformers import SentenceTransformer
# from langchain_core.documents import Document
# from app.services.embedding_model import embedding_model
# from app.core.settings import settings
# from app.core.logger import logger


# class EmbeddingService:

#     def __init__(self):

#         self.model = embedding_model

#     def embed_documents(
#         self,
#         documents: list[Document]
#     ) -> list[list[float]]:

#         logger.info(
#             f"Generating embeddings for {len(documents)} documents."
#         )

#         texts = [
#             document.page_content
#             for document in documents
#         ]

#         embeddings = self.model.encode(
#             texts,
#             normalize_embeddings=True,
#             show_progress_bar=True
#         )

#         logger.info("Document embeddings generated successfully.")

#         return embeddings.tolist()

#     def embed_query(
    #     self,
    #     query: str
    # ) -> list[float]:

    #     logger.info("Generating query embedding.")

    #     embedding = self.model.encode(
    #         query,
    #         normalize_embeddings=True
    #     )

    #     return embedding.tolist()



from langchain_core.documents import Document

from app.services.embedding_model import embedding_model
from app.core.logger import logger
import time


class EmbeddingService:

    def __init__(self):
        self.model = embedding_model

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

        BATCH_SIZE = 14
        embeddings = []

        total_batches = (
            len(texts) + BATCH_SIZE - 1
        ) // BATCH_SIZE

        for batch_number, start in enumerate(
            range(0, len(texts), BATCH_SIZE),
            start=1
        ):

            batch = texts[start:start + BATCH_SIZE]

            logger.info(
                f"Embedding batch {batch_number}/{total_batches} "
                f"({len(batch)} chunks)"
            )

            batch_embeddings = self.model.embed_documents(
                batch
            )

            embeddings.extend(batch_embeddings)

            time.sleep(4)

        logger.info(
            f"Generated {len(embeddings)} embeddings successfully."
        )

        return embeddings

    def embed_query(
        self,
        query: str
    ) -> list[float]:

        logger.info(
            "Generating query embedding."
        )

        embedding = self.model.embed_query(
            query
        )

        return embedding