from pydantic import BaseModel,HttpUrl

class IngestionRequest(BaseModel):
    repository_url:HttpUrl