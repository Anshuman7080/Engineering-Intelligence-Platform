from datetime import datetime, UTC

from fastapi import HTTPException, status

from app.repository.repository import RepositoryRepository


class RepositoryService:

    def __init__(self):

        self.repository_repository = RepositoryRepository()

    def create(
        self,
        user_id: str,
        repository_name: str,
        repository_url: str,
    ):

        if self.repository_repository.exists(
            user_id,
            repository_name,
        ):

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Repository already exists.",
            )

        return self.repository_repository.create(
            user_id=user_id,
            repository_name=repository_name,
            repository_url=repository_url,
        )

    def get(
        self,
        repository_id: str,
    ):

        repository = self.repository_repository.get(
            repository_id
        )

        if repository is None:

            raise HTTPException(
                status_code=404,
                detail="Repository not found.",
            )

        return repository

    def list(
        self,
        user_id: str,
    ):

        return self.repository_repository.list(
            user_id
        )

    def delete(
        self,
        repository_id: str,
    ):

        repository = self.repository_repository.get(
            repository_id
        )

        if repository is None:

            raise HTTPException(
                status_code=404,
                detail="Repository not found.",
            )

        self.repository_repository.delete(
            repository_id
        )

    def exists(
    self,
    user_id: str,
        repository_name: str,
    ) -> bool:

        return self.repository_repository.exists(
            user_id,
            repository_name,
        ) 
    
    