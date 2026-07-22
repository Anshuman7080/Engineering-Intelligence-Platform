from fastapi import APIRouter
from fastapi import HTTPException
from app.api.schemas.chat import (
    ChatRequest,
    ChatResponse,
    ConversationItem,
    ConversationResponse,
    ChatMessage
)

from app.pipelines.workflow_service import WorkflowService
from app.conversation.conversation_manager import ConversationManager

router = APIRouter()

workflow_service = WorkflowService()
conversation_manager=ConversationManager();


@router.post(
    "/question",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
):

    result = await workflow_service.ask(
        question=request.question,
        repository_id=request.repository_id,
        conversation_id=request.conversation_id,
    )

    return ChatResponse(
        conversation_id=result["conversation_id"],
        answer=result["answer"],
    )


@router.get(
    "/conversations/{repository_id}",
    response_model=list[ConversationItem],
)
async def list_conversations(
    repository_id: str,
):

    conversations = conversation_manager.list_conversations(
        repository_id
    )

    return [
        ConversationItem(
            id=c["id"],
            title=c["title"],
            updated_at=c["updated_at"].isoformat(),
        )
        for c in conversations
    ]

@router.get(
    "/conversation/{conversation_id}",
    response_model=ConversationResponse,
)

async def get_conversation(
    conversation_id: str,
):

    conversation = conversation_manager.get_conversation(
        conversation_id
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    history = conversation_manager.get_history(
        conversation_id
    )

    return ConversationResponse(
        id=conversation["id"],
        repository_id=conversation["repository_id"],
        title=conversation["title"],
        messages=[
            ChatMessage(**message)
            for message in history
        ]
    )



@router.delete(
    "/conversation/{conversation_id}",
)

async def delete_conversation(
    conversation_id:str,
):
    
    conversation_manager.delete_conversation(
        conversation_id
    )

    return {
        "success":True
    }