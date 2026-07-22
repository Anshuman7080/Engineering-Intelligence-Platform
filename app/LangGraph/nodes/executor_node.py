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

    print("=" * 80)
    print("Execution Plan")
    print(execution_plan.model_dump_json(indent=2))
    print("=" * 80)

    trace=state["trace_manager"]

    for step in execution_plan.steps:

        trace.add(
            node="Executor",
            title="Executing Tool",
            data={
                "tool":step.tool,
                "action":step.action,
                "arguments":step.arguments,
            }
        )

        tool = registry.get_tool(step.tool)

        if step.tool == ToolType.GRAPH:

            result = tool.execute(
                query_type=GraphQueryType(step.action),
                **step.arguments,
            )

        elif step.tool == ToolType.VECTOR:

            result = tool.execute(
                repository_id=state["repository_id"],
                **step.arguments,
            )

        else:

            raise ValueError(
                f"Unsupported tool: {step.tool}"
            )

        tool_results.append(result)

        trace.add(

            node="Executor",

            title="Tool Result",

            data=result.model_dump(),

        ) 

    state["tool_results"] = tool_results

    
    state["has_results"] = any(
        len(response.results) > 0
        for response in tool_results
    )

    return state