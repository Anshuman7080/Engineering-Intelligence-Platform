from app.agents.state import AgentState


async def fallback_node(state: AgentState):

    state["final_report"] = (
        "I couldn't find enough evidence "
        "inside the repository."
    )

    return state