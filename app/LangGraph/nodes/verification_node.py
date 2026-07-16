from app.agents.state import AgentState

from app.agents.verifier import Verifier


verifier = Verifier()


async def verification_node(
    state: AgentState,
):

    verification = await verifier.verify(
        question=state["question"],
        execution_plan=state["execution_plan"],
        tool_results=state["tool_results"],
    )

    state["verification"] = verification

    return state