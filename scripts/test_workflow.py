import asyncio

from app.LangGraph.workflow import workflow


async def main():

    result = await workflow.ainvoke(
        {
            "repository_name":"langchain.git",
            "question": "who calls anshuman()",
            "execution_plan": None,
            "tool_results": [],
            "verification": None,
            "reflection_count": 0,
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

    print("verification  result",result["verification"])


    print()
    print()
    print()


    print("Reflection count is",result["reflection_count"])


    print()
    print()
    print()

    print("final result is----->",result["final_report"])


asyncio.run(main())