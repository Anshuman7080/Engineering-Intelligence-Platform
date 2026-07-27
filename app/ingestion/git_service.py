from git import Repo, GitCommandError
from pathlib import Path

from app.core.logger import logger


class GitService:

    def clone_repository(self, repository_url: str, destination: str) -> Path:
        destination_path = Path(destination)

        if destination_path.exists():
            logger.info(f"Repository already exists: {destination_path}")
            return destination_path

        try:
            logger.info(f"Cloning repository: {repository_url}")


            repo=Repo.clone_from(repository_url, destination_path)
            try:
                return destination_path
            finally:
                repo.close()

        except GitCommandError as e:
            logger.error(f"Failed to clone repository: {e}")
            raise