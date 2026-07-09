from app.ingestion.loader import RepositoryLoader
from app.ingestion.chunker import DocumentChunker


loader=RepositoryLoader()
documents=loader.load("data/repositories/langchain")

print(f"Documents:{len(documents)}")

chunker=DocumentChunker()

chunks=chunker.split_documents(documents)

print(f"chunks:{len(chunks)}")

print()

print(chunks[0])

print(chunks[0].page_content)

print(chunks[0].metadata)
