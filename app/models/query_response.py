from pydantic import BaseModel


class Source(BaseModel):
    file: str
    score: float
    snippet: str


class QueryResponse(BaseModel):
    conversation_id: str
    question: str
    answer: str
    sources: list[Source]
    retrieved_chunks: int