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
        history=state["history"]
    )

    state["verification"] = verification

    trace=state["trace_manager"]
    trace.add(

        node="Verifier",

        title="Verification",

        data=verification.model_dump(),

    )

    return state