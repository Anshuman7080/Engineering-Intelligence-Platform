from app.llm.llm_service import LLMService

from app.prompts.verification_prompt import (
    VerificationPromptBuilder,
)

from app.parsing.verification_output_parser import (
    VerificationOutputParser,
)

from app.tools.evidence_formatter import (
    EvidenceFormatter,
)


class Verifier:

    def __init__(self):

        self.llm = LLMService()

    async def verify(
        self,
        question: str,
        execution_plan,
        tool_results,
    ):

        evidence = EvidenceFormatter.format(
            tool_results
        )

        system_prompt, user_prompt = (
            VerificationPromptBuilder.build(
                question=question,
                execution_plan=execution_plan,
                evidence=evidence,
            )
        )

        response = await self.llm.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        return VerificationOutputParser.parse(
            response
        )