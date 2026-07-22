import json

from app.agents.planning_models import ExecutionPlan


class PlannerOutputParser:

    @staticmethod
    def parse(
        response: str,
    ) -> ExecutionPlan:

        response = response.strip()

        if response.startswith("```"):

            lines = response.splitlines()

            if lines:
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            response = "\n".join(lines).strip()

        data = json.loads(response)

        return ExecutionPlan.model_validate(data)