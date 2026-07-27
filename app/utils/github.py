from urllib.parse import urlparse
import requests
from fastapi import HTTPException
BASE_URL = "https://api.github.com/repos"


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

 

def validate_python_repository(
        repository_name: str,
    ) -> None:

        url = f"{BASE_URL}/{repository_name}/languages"

        response = requests.get(url, timeout=10)

        if response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail="Repository not found.",
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=502,
                detail="Failed to validate repository language.",
            )

        languages = response.json()

        if not languages:
            raise HTTPException(
                status_code=400,
                detail="Unable to determine repository language.",
            )

        dominant_language = max(
            languages,
            key=languages.get,
        )

        if dominant_language != "Python":
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Detected '{dominant_language}' repository. "
                    "Only Python repositories are currently supported."
                ),
            )