from app.ingestion.git_service import GitService

git_service=GitService()

repository = git_service.clone_repository(
    repository_url="https://github.com/langchain-ai/langchain.git",
    destination="data/repositories/langchain"
)

print(repository)