from app.retrieval.retriever import Retriever
from app.llm.context_formatter import ContextFormatter
from app.llm.prompt_builder import PromptBuilder
from app.llm.llm_service import LLMService
from app.conversation.conversation_manager import ConversationManager


class QueryPipeline:

    def __init__(self):

        self.retriever = Retriever()
        self.llm_service = LLMService()
        self.conversation_manager = ConversationManager()

    async def ask(
        self,
        query: str,
        repository_name: str,
        conversation_id: str | None = None,
        top_k: int = 5,
    ):

        print("--------------------------------")
        print("conversation_id received:", conversation_id) 

        if not conversation_id:
            conversation_id = (
                self.conversation_manager.create_conversation()
            )
            print("conversation id is",conversation_id)


        self.conversation_manager.add_user_message(
            conversation_id,
            query,
        )


        history = self.conversation_manager.get_history(
            conversation_id
        )

        results = self.retriever.search(
            query=query,
            repository_name=repository_name,
            top_k=top_k,
        )


        context = ContextFormatter.format(results)


        system_prompt, user_prompt = PromptBuilder.build(
            query=query,
            context=context,
            history=history,
        )

        answer = await self.llm_service.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )


        self.conversation_manager.add_assistant_message(
            conversation_id,
            answer,
        )


        sources = []

        for result in results:
            source = result["metadata"].get("source")

            if source and source not in sources:
                sources.append(source)

        sources = list(dict.fromkeys(sources))[:3]

        return {
            "conversation_id": conversation_id,
            "question": query,
            "answer": answer,
            "sources": sources,
            "retrieved_chunks": len(results),
        }