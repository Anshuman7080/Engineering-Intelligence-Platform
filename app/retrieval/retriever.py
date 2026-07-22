from app.services.embedding_service import EmbeddingService
from app.services.pinecone_service import PineconeService


class Retriever:

    def __init__(self):

        self.embedding_service = EmbeddingService()
        self.pinecone_service = PineconeService()

    def search(
        self,
        query: str,
        user_id: str,
        repository_name: str,
        top_k: int = 5,
    ):

        query_embedding = self.embedding_service.embed_query(
            query
        )

        results = self.pinecone_service.similarity_search(
            embedding=query_embedding,
            user_id=user_id,
            repository_name=repository_name,
            top_k=top_k,
        )

        return results