from app.agents.state import AgentState


async def reflection_node(
    state: AgentState,
):
    
    state["reflection_count"] += 1
    print("Came in reflection node ------->>>",state["reflection_count"])

    return state