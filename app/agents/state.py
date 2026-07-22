from typing import TypedDict,Any


from app.tools.tool_response import ToolResponse
from app.agents.planning_models import ExecutionPlan
from app.agents.verification_models import (
    VerificationResult,
)

class AgentState(TypedDict):

    repository_id: str

    question: str

    execution_plan: ExecutionPlan | None

    tool_results: list[ToolResponse]

    verification: VerificationResult | None

    reflection_count: int

    final_report: str

    history: list[dict]

    conversation_id: str

    trace_manager: Any

    