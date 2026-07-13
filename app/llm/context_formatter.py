from typing import Any


class ContextFormatter:

    SEPARATOR = "\n" + "-" * 80 + "\n"

    @staticmethod
    def format(matches: list[Any]) -> str:
       

        if not matches:
            return 

        sections = []

        for index, match in enumerate(matches, start=1):

            metadata = getattr(match, "metadata", {}) or {}

            source = metadata.get("source", "Unknown")

            text = metadata.get("text", "").strip()

            score = getattr(match, "score", None)

            section = f"""
                Source {index}

                File:
                {source}

                Similarity:
                {score:.4f}

                Content:

                {text}
                """.strip()

            sections.append(section)

        return ContextFormatter.SEPARATOR.join(sections)