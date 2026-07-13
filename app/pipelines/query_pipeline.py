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

        for result in results[:3]:

            metadata = result["metadata"]

            sources.append(
                {
                    "file": metadata.get("source", ""),
                    "score": round(result["score"], 4),
                    "snippet": metadata.get("text", "")[:250],
                }
            )

        return {
            "conversation_id": conversation_id,
            "question": query,
            "answer": answer,
            "sources": sources,
            "retrieved_chunks": len(results),
        }