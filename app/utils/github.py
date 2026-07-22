from urllib.parse import urlparse


def extract_repository_name(repository_url: str) -> str:
    """
    https://github.com/langchain-ai/langchain.git
            ↓
    langchain-ai/langchain
    """

    path = urlparse(repository_url).path

    parts = [
        part
        for part in path.strip("/").split("/")
        if part
    ]

    if len(parts) < 2:
        raise ValueError("Invalid GitHub repository URL.")

    owner = parts[0]
    repository = parts[1].removesuffix(".git")

    return f"{owner}/{repository}"