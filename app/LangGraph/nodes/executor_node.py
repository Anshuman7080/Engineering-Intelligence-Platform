from app.agents.state import AgentState
from app.agents.tool_type import ToolType

from app.tools.tool_registry import ToolRegistry
from app.tools.graph_query_types import GraphQueryType


registry = ToolRegistry()


async def executor_node(
    state: AgentState,
) -> AgentState:

    execution_plan = state["execution_plan"]

    if execution_plan is None:
        return state

    tool_results = []

    for step in execution_plan.steps:

        tool = registry.get_tool(step.tool)

        if step.tool == ToolType.GRAPH:

            result = tool.execute(
                query_type=GraphQueryType(step.action),
                **step.arguments,
            )

        elif step.tool == ToolType.VECTOR:

            result = tool.execute(
                repository_name=state["repository_name"],
                **step.arguments,
            )

        else:

            raise ValueError(
                f"Unsupported tool: {step.tool}"
            )

        tool_results.append(result)

    state["tool_results"] = tool_results

    
    state["has_results"] = any(
        len(response.results) > 0
        for response in tool_results
    )

    return state