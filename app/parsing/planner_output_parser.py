import json

from app.agents.planning_models import ExecutionPlan

class PlannerOutputParser:

    @staticmethod
    def parse(
        response: str,
    ) -> ExecutionPlan:

        data = json.loads(response)

        return ExecutionPlan.model_validate(data)