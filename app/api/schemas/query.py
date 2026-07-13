from pydantic import BaseModel

class QueryRequest(BaseModel):
    repository_name:str
    question:str
    conversation_id:str | None=None
    top_k:int=5
    