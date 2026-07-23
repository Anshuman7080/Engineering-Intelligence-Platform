import json

from app.agents.planning_models import ExecutionPlan


class PlannerOutputParser:

    @staticmethod
    def parse(response: str) -> ExecutionPlan:

        response = response.strip()

       
        if "```" in response:
            start = response.find("```")
            end = response.rfind("```")

            if start != -1 and end != start:
                response = response[start + 3:end]

                if response.startswith("json"):
                    response = response[4:]

                response = response.strip()

        data = json.loads(response)

   
        for step in data.get("steps", []):

            if isinstance(step.get("tool"), str):
                step["tool"] = step["tool"].strip().lower()

            if isinstance(step.get("action"), str):
                step["action"] = step["action"].strip().lower()

        return ExecutionPlan.model_validate(data)