from app.agents.state import AgentState
from app.agents.verification_models import VerificationDecision

MAX_REFLECTIONS = 2


def route_after_verification(
    state: AgentState,
):

    verification = state["verification"]

    if verification is None:
        return "stop"

    if verification.decision == VerificationDecision.ANSWER:
        return "report"

    if verification.decision == VerificationDecision.STOP:
        return "stop"

    if state["reflection_count"] >= MAX_REFLECTIONS:
        return "stop"

    return "reflection"