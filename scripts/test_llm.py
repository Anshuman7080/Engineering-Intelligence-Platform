import asyncio

from app.llm.prompt_builder import PromptBuilder
from app.llm.llm_service import LLMService


async def main():

    context = [
        """
Source: README.md

LangChain is a framework for building agents.
"""
    ]

    system_prompt, user_prompt = PromptBuilder.build(
        query="What is LangChain?",
        context=context,
    )

    llm = LLMService()

    answer = await llm.generate(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )

    print("\n===== LLM RESPONSE =====\n")
    print(answer)


if __name__ == "__main__":
    asyncio.run(main())