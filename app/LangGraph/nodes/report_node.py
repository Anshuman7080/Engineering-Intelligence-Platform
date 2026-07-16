from app.agents.state import AgentState
from app.agents.report_generator import ReportGenerator

from app.tools.evidence_formatter import EvidenceFormatter

generator=ReportGenerator()

async def report_node(
        state:AgentState,
):
    
    evidence=EvidenceFormatter.format(
        state["tool_results"]
    )

    report=await generator.generate(
        question=state["question"],
        evidence=evidence,
        verification=state["verification"],
    )

    state["final_report"]=report

    return state