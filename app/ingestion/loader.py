from pathlib import Path
from langchain_core.documents import Document

from app.core.logger import logger


SUPPORTED_EXTENSIONS = {
    ".py",
    ".md",
    ".txt",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
}

IGNORED_DIRECTORIES = {
    ".git",
    "__pycache__",
    "node_modules",
    ".pytest_cache",
    ".venv",
    "venv",
    "dist",
    "build",
}


class RepositoryLoader:

    def load(self, repository_path: str):

        documents = []

        repository = Path(repository_path)

       

        for file in repository.rglob("*"):


            if not file.is_file():
                continue

            if any(
                part in IGNORED_DIRECTORIES
                for part in file.parts
            ):
                continue

            if file.suffix not in SUPPORTED_EXTENSIONS:
                continue

            try:

                content = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                document = Document(
                    page_content=content,
                    metadata={
                        "source": str(file),
                        "extension": file.suffix,
                        "file_name": file.name,
                    }
                )

                documents.append(document)

            except Exception as e:

                logger.warning(f"Failed to read {file}: {e}")

        logger.info(f"Loaded {len(documents)} documents")

        return documents