from app.agents.planner import Planner
from app.agents.state import AgentState

planner = Planner()


async def planner_node(
    state: AgentState,
) -> AgentState:

    plan = await planner.plan(
        state["question"]
    )

    state["execution_plan"] = plan

    return state