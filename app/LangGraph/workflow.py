from langgraph.graph import StateGraph
from langgraph.graph import START, END

from app.agents.state import AgentState
from app.LangGraph.nodes.planner_node import planner_node


builder = StateGraph(AgentState)

builder.add_node(
    "planner",
    planner_node,
)

builder.add_edge(
    START,
    "planner",
)

builder.add_edge(
    "planner",
    END,
)

workflow = builder.compile()