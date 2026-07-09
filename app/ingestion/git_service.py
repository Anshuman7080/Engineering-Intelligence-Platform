from pathlib import Path

from git import Repo

from app.core.logger import logger


class GitService:

    def clone_repository(
        self,
        repository_url: str,
        destination: str
    ) -> Path:

        destination_path = Path(destination)

        if destination_path.exists():
            logger.info(
                f"Repository already exists at {destination_path}"
            )
            return destination_path

        logger.info(
            f"Cloning repository: {repository_url}"
        )

        Repo.clone_from(
            repository_url,
            destination_path
        )

        logger.info("Repository cloned successfully.")

        return destination_path