import json

from app.tools.tool_response import ToolResponse


class EvidenceFormatter:

    @staticmethod
    def format(
        responses: list[ToolResponse],
    ) -> str:

        sections = []

        for response in responses:

            sections.append(
                f"""
Tool: {response.tool}

Query: {response.query_type}

Results:

{json.dumps(response.results, indent=2, default=str)}
""".strip()
            )

        return "\n\n".join(sections)