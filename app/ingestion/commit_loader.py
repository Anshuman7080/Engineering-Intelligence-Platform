from pathlib import Path
import subprocess

from langchain_core.documents import Document

from app.core.logger import logger


class CommitLoader:

    def load(
        self,
        repository_path: str | Path,
    ) -> list[Document]:

        logger.info("Loading git commits...")

        repository_path = Path(repository_path)

        command = [
            "git",
            "-C",
            str(repository_path),
            "log",
            "--pretty=format:%H|%an|%ad|%s",
            "--date=iso",
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
        )

        documents = []

        for line in result.stdout.splitlines():

            parts = line.split("|", 3)

            if len(parts) != 4:
                continue

            sha, author, date, message = parts

            documents.append(
                Document(
                    page_content=message,
                    metadata={
                        "artifact_type": "commit",
                        "sha": sha,
                        "author": author,
                        "date": date,
                        "repository": repository_path.name,
                        "source": f"commit:{sha}",
                    },
                )
            )

        logger.info(
            f"Loaded {len(documents)} commits."
        )

        return documents