REPORT_SYSTEM_PROMPT = """
You are the final reporting component of an AI Engineering Intelligence Platform.

You are NOT responsible for deciding whether the evidence is sufficient.
That decision has already been made by the verifier.

Your job is to generate the final response using:

- the user's question
- the verification result
- the collected evidence

Rules

1. Never hallucinate.

2. Use ONLY the provided evidence.

3. Never contradict the verification decision.

4. If the decision is "answer", produce the best possible answer using the evidence.

5. If the decision is "stop", clearly explain that the repository does not contain enough verified evidence to answer the question.

6. Mention filenames whenever possible.

7. If multiple files contribute, mention all of them.

8. Keep the response concise but complete.
""".strip()


class ReportPromptBuilder:

    @staticmethod
    def build(
        question: str,
        evidence: str,
        verification,
    ):

        user_prompt = f"""
Question

{question}

{"=" * 80}

Verification

Decision:
{verification.decision.value}

Confidence:
{verification.confidence}

Reasoning:
{verification.reasoning}

Missing Information:
{verification.missing_information}

{"=" * 80}

Evidence

{evidence}

{"=" * 80}

Generate the final response.
""".strip()

        return (
            REPORT_SYSTEM_PROMPT,
            user_prompt,
        )