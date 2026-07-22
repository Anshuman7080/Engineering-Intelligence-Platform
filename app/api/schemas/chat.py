from pydantic import BaseModel


class ChatRequest(BaseModel):

    question: str

    repository_id: str

    conversation_id: str | None = None


class ChatResponse(BaseModel):

    conversation_id: str

    answer: str


class ConversationSummary(BaseModel):

    id: str

    title: str

    repository_id: str

    created_at: str

    updated_at: str


class ConversationHistoryResponse(BaseModel):

    conversation_id: str

    messages: list[dict]

class ConversationItem(BaseModel):
    id:str
    title:str
    updated_at:str    

class ChatMessage(BaseModel):
    role:str
    content:str


class ConversationResponse(BaseModel):
    id:str
    repository_id:str
    title:str
    messages:list[ChatMessage]
    