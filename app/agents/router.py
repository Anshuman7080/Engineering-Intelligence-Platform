from app.agents.state import AgentState
from app.agents.verification_models import VerificationDecision

MAX_REFLECTIONS = 2


def route_after_verification(
    state: AgentState,
):

    verification = state["verification"]
    trace = state["trace_manager"]

    if verification is None:

        decision = "NONE"

    else:

        decision = verification.decision.value

    if verification is None:

        trace.add(
            node="Reflection",
            title="Workflow Finished",
            data={
                "decision": decision
            }
        )

        return "stop"

    if verification.decision == VerificationDecision.ANSWER:
        return "report"

    if (
        verification.decision == VerificationDecision.STOP
        or state["reflection_count"] >= MAX_REFLECTIONS
    ):

        trace.add(
            node="Reflection",
            title="Workflow Finished",
            data={
                "decision": decision
            }
        )

        return "stop"

    return "reflection"