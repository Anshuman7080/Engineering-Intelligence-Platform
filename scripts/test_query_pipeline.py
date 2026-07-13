import asyncio

from app.pipelines.query_pipeline import QueryPipeline


async def main():

    pipeline = QueryPipeline()

    result = await pipeline.ask(
        query="What is LangChain?",
        repository_name="langchain.git",
    )

    print("\nAnswer:\n")
    print(result["answer"])

    print("\nSources:\n")
    for source in result["sources"]:
        print(source)


if __name__ == "__main__":
    asyncio.run(main())