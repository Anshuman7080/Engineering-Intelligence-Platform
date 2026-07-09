from app.ingestion.loader import RepositoryLoader

loader=RepositoryLoader()

documents=loader.load("data/repositories/langchain")

print(f"TotalDocuments:{len(documents)}")

print()

print(documents[0])