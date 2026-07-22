from datetime import datetime

from pydantic import BaseModel


class RepositoryCreateRequest(BaseModel):

    repository_url: str


class RepositoryResponse(BaseModel):

    id: str

    repository_name: str

    repository_url: str

    created_at: datetime

    last_ingested: datetime