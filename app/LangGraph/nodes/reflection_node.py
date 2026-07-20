from app.agents.state import AgentState


async def reflection_node(
    state: AgentState,
):
    
    state["reflection_count"] += 1
    trace=state["trace_manager"]
    verification=state["verification"]

    print("Came in reflection node ------->>>",state["reflection_count"])
    trace.add(

    node="Reflection",

    title="Retry",

    data={

        "reason": verification.reasoning,

        "reflection_count": state["reflection_count"],

    }

)
    return state