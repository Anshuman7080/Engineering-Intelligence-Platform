from app.ingestion.loader import RepositoryLoader
from app.ingestion.chunker import DocumentChunker
from app.services.embedding_service import EmbeddingService


def main():

  
    loader = RepositoryLoader()
    documents = loader.load("data/repositories/langchain")

    print(f"\nLoaded Documents: {len(documents)}")

 
    chunker = DocumentChunker()
    chunks = chunker.split_documents(documents)

    print(f"Generated Chunks: {len(chunks)}")


    embedding_service = EmbeddingService()


    embeddings = embedding_service.embed_documents(chunks[:5])

    print(f"\nGenerated Embeddings: {len(embeddings)}")

    print(f"Embedding Dimension: {len(embeddings[0])}")

    print("\nFirst 10 values of first embedding:")

    print(embeddings[0][:10])


if __name__ == "__main__":
    main()