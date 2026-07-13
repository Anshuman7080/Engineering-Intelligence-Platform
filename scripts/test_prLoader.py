from app.ingestion.pr_loader import PullRequestLoader

loader = PullRequestLoader()

prs = loader.load(
    "https://github.com/langchain-ai/langchain"
)

print(len(prs))
print(prs[0].metadata)
print(prs[0].page_content)