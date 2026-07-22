from uuid import uuid4

from app.LangGraph.workflow import workflow
from app.conversation.conversation_manager import ConversationManager
from app.tracing.trace_manager import TraceManager
from fastapi import HTTPException, status

from app.repository.repository import RepositoryRepository

class WorkflowService:

    def __init__(self):

        self.conversation_manager = ConversationManager()
        self.repository_repository = RepositoryRepository()

    async def ask(
        self,
        question: str,
        repository_id: str,
        user_id:str,
        conversation_id: str | None = None,
    ):
        repository = self.repository_repository.get(
            repository_id
        )

        if repository is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Repository not found.",
            )

        if repository.user_id != user_id:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this repository.",
            )

        if conversation_id is None:

            conversation_id = (
                self.conversation_manager.create_conversation(
                    repository_id=repository_id,
                    title=question,
                )
            )

        self.conversation_manager.add_user_message(
            conversation_id,
            question,
        )

        if conversation_id is not None:

            conversation = self.conversation_manager.get_conversation(
                conversation_id,
                user_id,
            )

            if conversation is None:

                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found.",
                )

        history = (
            self.conversation_manager.get_history(
                conversation_id
            )
        )

        trace_id = str(uuid4())

        trace_manager = TraceManager()

        state = {

            "question": question,

            "user_id": repository.user_id,

            "repository_name": repository.repository_name,

            "repository_id": repository_id,

            "history": history,

            "conversation_id": conversation_id,

            "execution_plan": None,

            "tool_results": [],

            "verification": None,

            "reflection_count": 0,

            "has_results": False,

            "final_report": "",

            "trace_manager": trace_manager,
        }

        result = await workflow.ainvoke(
            state
        )

        trace_manager.save(trace_id)

        self.conversation_manager.add_assistant_message(
            conversation_id,
            result["final_report"],
        )

        return {
            "conversation_id": conversation_id,
            "answer": result["final_report"],
        }