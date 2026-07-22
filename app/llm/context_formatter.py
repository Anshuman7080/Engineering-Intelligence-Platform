from typing import Any


class ContextFormatter:

    SEPARATOR = "\n" + "-" * 80 + "\n"

    @staticmethod
    def format(matches: list[Any]) -> str:

        if not matches:
            return ""

        sections = []

        for index, match in enumerate(matches, start=1):

            metadata = getattr(match, "metadata", {}) or {}

            source = metadata.get("source", "Unknown")

            text = metadata.get("text", "").strip()

            score = getattr(match, "score", None)

            similarity = (
                f"{score:.4f}"
                if score is not None
                else "N/A"
            )

            section = f"""
            Source {index}

            File:
            {source}

            Similarity:
            {similarity}

            Content:

            {text}
            """.strip()

            sections.append(section)

        return ContextFormatter.SEPARATOR.join(sections)