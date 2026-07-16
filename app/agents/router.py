

def route_after_execution(state):

    if state["has_results"]:
        return "report"

    return "fallback"