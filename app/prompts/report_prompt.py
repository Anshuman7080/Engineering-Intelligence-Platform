REPORT_SYSTEM_PROMPT = """
You are the final reporting component of an AI Engineering Intelligence Platform.

You are NOT responsible for deciding whether the evidence is sufficient.
That decision has already been made by the verifier.

Your job is to generate the final response using:

- the conversation history
- the user's current question
- the verification result
- the collected evidence

Rules

1. Never hallucinate.

2. Use ONLY the provided evidence.

3. Use the conversation history only to understand the user's intent and references.

4. Never use conversation history as factual evidence.

5. Never contradict the verification decision.

6. If the decision is "answer", produce the best possible answer using the evidence.

7. If the decision is "stop", clearly explain that the repository does not contain enough verified evidence to answer the question.

8. Mention filenames whenever possible.

9. If multiple files contribute, mention all of them.

10. Keep the response concise but complete.
""".strip()

class ReportPromptBuilder:

    @staticmethod
    def build(
        question: str,
        evidence: str,
        verification,
        history: list[dict],
    ):

        history_text = ""

        for message in history:
            history_text += (
                f'{message["role"].capitalize()}: '
                f'{message["content"]}\n'
            )

        if verification is None:

            decision = "stop"
            confidence = 0.0
            reasoning = (
                "No verification result was produced."
            )
            missing_information = (
                "Insufficient verified evidence."
            )

        else:

            decision = verification.decision.value
            confidence = verification.confidence
            reasoning = verification.reasoning
            missing_information = (
                verification.missing_information
            )

        user_prompt = f"""
Conversation History

{history_text}

{"=" * 80}

Question

{question}

{"=" * 80}

Verification

Decision:
{decision}

Confidence:
{confidence}

Reasoning:
{reasoning}

Missing Information:
{missing_information}

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