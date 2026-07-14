from pathlib import Path

from app.parsing.ast_parser import ASTParser
from app.parsing.import_extractor import ImportExtractor
from app.parsing.class_extractor import ClassExtractor
from app.parsing.function_extractor import FunctionExtractor
from app.parsing.call_extractor import CallExtractor
from app.core.logger import logger


class RepositoryParser:

    def __init__(self):

        self.ast_parser = ASTParser()

        self.import_extractor = ImportExtractor()
        self.class_extractor = ClassExtractor()
        self.function_extractor = FunctionExtractor()
        self.call_extractor = CallExtractor()

    def parse_repository(
        self,
        repository_path: str | Path,
    ) -> dict:

        repository_path = Path(repository_path)

        repository = {
            "files": []
        }

        python_files = list(
            repository_path.rglob("*.py")
        )

        logger.info(
            f"Found {len(python_files)} Python files."
        )

        for file_path in python_files:

            parsed_file = self.parse_file(
                file_path=file_path,
                repository_path=repository_path,
            )

            if parsed_file is not None:
                repository["files"].append(parsed_file)

        logger.info(
            f"Parsed {len(repository['files'])} files."
        )

        return repository

    def parse_file(
        self,
        file_path: Path,
        repository_path: Path,
    ) -> dict | None:

        try:

            tree = self.ast_parser.parse(
                file_path=file_path,
            )

        except SyntaxError:

            logger.warning(
                f"Skipping file with syntax error: {file_path}"
            )

            return None

        except Exception as e:

            logger.warning(
                f"Failed to parse {file_path}: {e}"
            )

            return None

        return {

            "path": str(
                file_path.relative_to(repository_path)
            ),

            "imports": self.import_extractor.extract(tree),

            "classes": self.class_extractor.extract(tree),

            "functions": self.function_extractor.extract(tree),

            "calls": self.call_extractor.extract(tree),
        }