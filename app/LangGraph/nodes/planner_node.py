from app.agents.planner import Planner
from app.agents.state import AgentState

planner = Planner()


async def planner_node(
    state: AgentState,
) -> AgentState:

    plan = await planner.plan(
        question=state["question"],
        previous_plan=state["execution_plan"],
        verification=state["verification"],
        history=state["history"]
    )

    state["execution_plan"] = plan

    trace=state["trace_manager"]

    trace.add(
        node="Planner",
        title="Execution Plan",
        data=plan.model_dump()
    )

    return state