import asyncio

from app.LangGraph.workflow import workflow


async def main():

    result = await workflow.ainvoke(
        {
            "question": "Who calls invoke()?",
            "execution_plan": None,
            "tool_results": [],
            "final_report": "",
        }
    )

    print(result["execution_plan"])


asyncio.run(main())