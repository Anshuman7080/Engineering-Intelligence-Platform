from app.llm.llm_service import LLMService

from app.prompts.planner_prompt import PlannerPromptBuilder

from app.parsing.planner_output_parser import PlannerOutputParser

from app.agents.planning_models import ExecutionPlan
from app.agents.verification_models import VerificationResult


class Planner:

    def __init__(self):

        self.llm = LLMService()

    async def plan(
        self,
        question: str,
        history: list[dict],
        previous_plan: ExecutionPlan | None = None,
        verification: VerificationResult | None = None,
        
    ):

        system_prompt, user_prompt = (
            PlannerPromptBuilder.build(
                question=question,
                previous_plan=previous_plan,
                verification=verification,
                history=history,
            )

        )

        response = await self.llm.generate(
            system_prompt,
            user_prompt,
        )

        return PlannerOutputParser.parse(
            response
        )