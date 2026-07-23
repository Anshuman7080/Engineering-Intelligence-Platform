from langchain_core.documents import Document
import requests

from app.core.logger import logger


class PullRequestLoader:

    def load(
        self,
        repository_url: str,
    ) -> list[Document]:

        logger.info("Loading pull requests...")

        owner, repo = repository_url.rstrip("/").split("/")[-2:]
        repo = repo.removesuffix(".git")

        url = (
            f"https://api.github.com/repos/"
            f"{owner}/{repo}/pulls"
        )

        try:

            response = requests.get(
                url,
                params={
                    "state": "all",
                    "per_page": 100,
                },
                headers={
                    "Accept": "application/vnd.github+json",
                },
                timeout=30,
            )

            response.raise_for_status()

        except requests.RequestException as e:

            logger.exception(
                f"Failed to fetch pull requests for {owner}/{repo}: {e}"
            )

            # Continue ingestion without PR documents
            return []

        prs = response.json()

        documents = []

        for pr in prs:

            text = f"""
Title:
{pr['title']}

Description:
{pr.get('body') or ''}
"""

            documents.append(
                Document(
                    page_content=text.strip(),
                    metadata={
                        "artifact_type": "pull_request",
                        "repository": repo,
                        "source": pr["html_url"],
                        "number": pr["number"],
                        "state": pr["state"],
                        "author": pr["user"]["login"],
                        "created_at": pr["created_at"],
                    },
                )
            )

        logger.info(
            f"Loaded {len(documents)} pull requests."
        )

        return documents