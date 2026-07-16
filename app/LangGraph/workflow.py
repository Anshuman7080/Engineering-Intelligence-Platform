from langgraph.graph import StateGraph
from langgraph.graph import START, END

from app.agents.state import AgentState
from app.LangGraph.nodes.planner_node import planner_node
from app.LangGraph.nodes.executor_node import executor_node
from app.LangGraph.nodes.report_node import report_node

from app.agents.router import route_after_execution

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

builder.add_node(
    "fallback",
    fallback_node
)

builder.add_conditional_edges(
    "executor",
    route_after_execution,
    {
        "report":"report",
        "fallback":"fallback",
    }
    
)


builder.add_edge(
    "fallback",
    END,
)


builder.add_edge(
    "report",
    END,
)

workflow = builder.compile()