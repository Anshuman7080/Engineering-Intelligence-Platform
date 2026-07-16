REPORT_SYSTEM_PROMPT = """
You are an expert software engineer.

You answer questions ONLY using the provided evidence.

Rules

1. Never hallucinate.

2. Use ONLY the evidence.

3. If the evidence is insufficient, clearly say so.

4. Mention filenames whenever possible.

5. If multiple sources contribute, mention all of them.

6. Write a concise but complete answer.
""".strip()


class ReportPromptBuilder:

    @staticmethod
    def build(
        question: str,
        evidence: str,
    ):

        user_prompt = f"""
Question

{question}

Evidence

{evidence}

Answer:
""".strip()

        return (
            REPORT_SYSTEM_PROMPT,
            user_prompt,
        )