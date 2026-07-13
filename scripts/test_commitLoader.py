from app.ingestion.commit_loader import CommitLoader

loader = CommitLoader()

docs = loader.load("data/repositories/langchain.git")

print(len(docs))

print(docs[0].page_content)

print(docs[0].metadata)