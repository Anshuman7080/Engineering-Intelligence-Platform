from typing import TypedDict

from app.tools.tool_response import ToolResponse
from app.agents.planning_models import ExecutionPlan

class AgentState(TypedDict):

    question: str

    execution_plan: ExecutionPlan | None

    tool_results: list[ToolResponse]

    final_report: str