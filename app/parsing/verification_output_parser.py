import json

from app.agents.verification_models import VerificationResult


class VerificationOutputParser:

    @staticmethod
    def parse(
        response: str,
    ) -> VerificationResult:

        response = response.strip()

        if response.startswith("```"):

            response = (
                response.replace("```json", "")
                .replace("```", "")
                .strip()
            )

        data = json.loads(response)

        return VerificationResult(**data)