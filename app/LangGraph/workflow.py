from langgraph.graph import StateGraph
from langgraph.graph import START, END

from app.agents.state import AgentState
from app.LangGraph.nodes.planner_node import planner_node
from app.LangGraph.nodes.executor_node import executor_node
from app.LangGraph.nodes.report_node import report_node

builder = StateGraph(AgentState)

builder.add_node(
    "planner",
    planner_node,
)

builder.add_edge(
    START,
    "planner",
)

builder.add_node(
    "executor",
    executor_node
)

builder.add_edge(
    "planner",
    "executor",
)


builder.add_node(
    "report",
    report_node,
)

builder.add_edge(
    "executor",
    "report",
)



builder.add_edge(
    "report",
    END,
)

workflow = builder.compile()