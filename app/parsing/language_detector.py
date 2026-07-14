from pathlib import Path


class LanguageDetector:

    LANGUAGE_MAP = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".tsx": "typescript",
        ".jsx": "javascript",
        ".java": "java",
        ".go": "go",
        ".cpp": "cpp",
        ".cc": "cpp",
        ".cxx": "cpp",
        ".c": "c",
        ".cs": "csharp",
    }

    @classmethod
    def detect(cls, file_path: str | Path) -> str | None:

        suffix = Path(file_path).suffix.lower()

        return cls.LANGUAGE_MAP.get(suffix)