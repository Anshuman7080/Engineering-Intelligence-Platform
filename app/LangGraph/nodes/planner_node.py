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
    )

    state["execution_plan"] = plan

    return state