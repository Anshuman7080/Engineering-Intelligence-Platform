VERIFICATION_SYSTEM_PROMPT = """
You are the verification component of an AI Engineering Intelligence Platform.

You are NOT answering the user's question.

Your job is to verify whether the collected evidence actually supports answering the question.

Carefully inspect:

1. User question
2. Conversation history
3. Execution plan
4. Tool outputs

Determine:

- Is the evidence sufficient?
- Is the evidence relevant?
- Is more investigation required?
- Is the repository unlikely to contain the answer?

Decision Guidelines

Return "answer" if:

• Evidence sufficiently answers the question.

Return "retry" if:

• A different investigation strategy could reasonably obtain better evidence.
• The planner likely chose the wrong tool or query.

Return "stop" if:

• The repository is unlikely to contain the answer.
• The question is unrelated to the repository.
• Additional retries are unlikely to improve the result.

When evaluating the current question, use the conversation history to resolve
references such as "it", "that", "this", "they", "the previous function", etc.

The latest user question always has the highest priority.

Return ONLY valid JSON.

Schema

{
    "supported": true,
    "confidence": 87,
    "reasoning": "...",
    "missing_information": [],
    "decision": "answer"
}
""".strip()


class VerificationPromptBuilder:

    @staticmethod
    def build(
        question: str,
        execution_plan,
        evidence: str,
        history: list[dict],
    ):

        user_prompt = f"""
Conversation History

{history}

============================================================

Current Question

{question}

============================================================

Execution Plan

{execution_plan.model_dump_json(indent=2)}

============================================================

Tool Results

{evidence}

============================================================

Verification:
""".strip()

        return (
            VERIFICATION_SYSTEM_PROMPT,
            user_prompt,
        )