from app.llm.prompts import SYSTEM_PROMPT


class PromptBuilder:

    @staticmethod
    def build(
    query: str,
    context: list[str],
    history: list[dict],
    )-> tuple[str, str]:
        

        history_text=""

        for message in history:
            history_text += (
                f'{message["role"].capitalize()}: '
                f'{message["content"]}\n'
            )

        user_prompt = f"""
         
        Conversation History

        {history_text}

        {"=" * 80}


        Repository Context

        {context}

        {"=" * 80}

        Question

        {query}

        Answer:
        """.strip()

        return SYSTEM_PROMPT, user_prompt