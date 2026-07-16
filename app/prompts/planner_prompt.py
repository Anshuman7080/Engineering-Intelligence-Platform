PLANNER_SYSTEM_PROMPT = """
You are the planning component of an AI Engineering Intelligence Platform.

Your task is NOT to answer the question.

Your task is ONLY to generate an execution plan.


The execution plan may contain one or more steps.

Use as many steps as necessary.

If multiple tools are required,
return them in the correct execution order.

Do NOT answer the question.

Only produce the plan.


Available Tools

GRAPH

Supported Actions

- find_symbol
- find_callers
- find_callees
- find_dependencies
- find_importers
- find_commits_for_file
- find_files_for_commit
- find_issue_commits
- find_issue_changes

VECTOR

Supported Actions

- semantic_search

Rules

1. Return ONLY valid JSON.
2. Do not use markdown.
3. Do not wrap JSON inside ``` blocks.
4. Do not explain anything.

Output Schema

{
    "reasoning": "...",
    "steps":[
        {
            "tool":"graph",
            "action":"find_callers",
            "arguments":{
                "symbol_name":"Runnable.invoke"
            }
        }
    ]
}
""".strip()

class PlannerPromptBuilder:

    @staticmethod
    def build(
        question: str,
        previous_plan=None,
        verification=None,
    ):

        if (
            previous_plan is None
            or verification is None
        ):

            user_prompt = f"""
                Question

                {question}

                Execution Plan:
                """.strip()

            return (
                PLANNER_SYSTEM_PROMPT,
                user_prompt,
            )

        user_prompt = f"""
Question

{question}

{"=" * 80}

Previous Execution Plan

{previous_plan.model_dump_json(indent=2)}

{"=" * 80}

Verification Feedback

Reasoning

{verification.reasoning}

Confidence

{verification.confidence}

Missing Information

{verification.missing_information}

{"=" * 80}

The previous investigation was not sufficient.

Generate a better execution plan.

Execution Plan:
""".strip()

        return (
            PLANNER_SYSTEM_PROMPT,
            user_prompt,
        )