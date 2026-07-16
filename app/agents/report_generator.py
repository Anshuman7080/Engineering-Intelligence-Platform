from app.llm.llm_service import LLMService

from app.prompts.report_prompt import (
    ReportPromptBuilder,
)
from app.parsing.report_output_parser import (
    ReportOutputParser
)


class ReportGenerator:

    def __init__(self):
        self.llm = LLMService()

    async def generate(
            self,
            question:str,
            evidence:str,
            verification,
    ):
        
        system_prompt,user_prompt=(
            ReportPromptBuilder.build(
                question,
                evidence,
                verification
            )
        )

        response=await self.llm.generate(
            system_prompt,
            user_prompt,
        )


        return ReportOutputParser.parse(
            response
        )
            