from app.LangGraph.workflow import workflow

from app.conversation.conversation_manager import ConversationManager


class WorkflowService:

    def __init__(self):

        self.conversation_manager = ConversationManager()

    async def ask(
        self,
        question: str,
        repository_name: str,
        conversation_id: str | None = None,
    ):

        if not conversation_id:

            conversation_id = (
                self.conversation_manager.create_conversation(
                    repository_name=repository_name,
                    title=question,
                )
            )

        self.conversation_manager.add_user_message(
            conversation_id,
            question,
        )

        history = (
            self.conversation_manager.get_history(
                conversation_id
            )
        )

        state = {

            "question": question,

            "repository_name": repository_name,

            "history": history,

            "conversation_id": conversation_id,

            "execution_plan": None,

            "tool_results": [],

            "verification": None,

            "reflection_count": 0,

            "has_results": False,

            "final_report": "",
        }

        result = await workflow.ainvoke(
            state
        )

        self.conversation_manager.add_assistant_message(
            conversation_id,
            result["final_report"],
        )

        return {
            "conversation_id": conversation_id,
            "answer": result["final_report"],
        }