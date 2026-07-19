from langgraph.graph import StateGraph
from langgraph.graph import START, END

from app.agents.state import AgentState

from app.LangGraph.nodes.planner_node import planner_node
from app.LangGraph.nodes.executor_node import executor_node
from app.LangGraph.nodes.verification_node import verification_node
from app.LangGraph.nodes.reflection_node import reflection_node
from app.LangGraph.nodes.report_node import report_node

from app.agents.router import route_after_verification


builder = StateGraph(AgentState)


builder.add_node(
    "planner",
    planner_node,
)

builder.add_node(
    "executor",
    executor_node,
)

builder.add_node(
    "verification",
    verification_node,
)

builder.add_node(
    "reflection",
    reflection_node,
)

builder.add_node(
    "report",
    report_node,
)


builder.add_edge(
    START,
    "planner",
)

builder.add_edge(
    "planner",
    "executor",
)

builder.add_edge(
    "executor",
    "verification",
)


builder.add_conditional_edges(
    "verification",
    route_after_verification,
    {
        "report": "report",
        "reflection": "reflection",
        "stop": "report",
    },
)


builder.add_edge(
    "reflection",
    "planner",
)

builder.add_edge(
    "report",
    END,
)


workflow = builder.compile()