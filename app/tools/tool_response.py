from dataclasses import dataclass
from typing import Any


@dataclass
class ToolResponse:

    tool: str
    query_type: str
    results: list[Any]