from typing import Any

from pydantic import BaseModel

from app.agents.tool_type import ToolType


class PlanStep(BaseModel):

    tool: ToolType

    action: str

    arguments: dict[str, Any]


class ExecutionPlan(BaseModel):

    reasoning: str

    steps: list[PlanStep]