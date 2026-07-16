from app.llm.llm_service import LLMService

from app.prompts.planner_prompt import PlannerPromptBuilder

from app.parsing.planner_output_parser import PlannerOutputParser


class Planner:

    def __init__(self):

        self.llm = LLMService()

    async def plan(
       self,
    question: str,
    ):

        system_prompt, user_prompt = (
            PlannerPromptBuilder.build(
                question
            )
        )

        response = await self.llm.generate(
            system_prompt,
            user_prompt,
        )

        return PlannerOutputParser.parse(
            response
        )    