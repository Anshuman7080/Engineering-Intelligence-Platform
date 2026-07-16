import asyncio

from app.LangGraph.workflow import workflow


async def main():

    result = await workflow.ainvoke(
        {
            "repository_name":"langchain.git",
            "question": "Explain how Runnable.invoke() works.",
            "execution_plan": None,
            "tool_results": [],
            "final_report": "",
        }
    )

   
    print("execution plan is",result["execution_plan"])

    print()
    print()
    print()

    print("tool execution result",result["tool_results"])
    
    print()
    print()
    print()

    print(result["final_report"])


asyncio.run(main())