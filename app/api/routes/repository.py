from fastapi import APIRouter, Depends, HTTPException


from app.api.dependencies.auth import get_current_user
from app.api.schemas.repository import (
    RepositoryCreateRequest,
    RepositoryResponse,
)
from app.utils.github import extract_repository_name

from app.repository.repository_service import RepositoryService
from app.services.repository_cleanup_service import RepositoryCleanupService
router = APIRouter()

repository_service = RepositoryService()
repository_cleanup_service=RepositoryCleanupService()


@router.post(
    "/",
    response_model=RepositoryResponse,
)
async def create_repository(
    request: RepositoryCreateRequest,
    current_user=Depends(
        get_current_user
    ),
):

    repository_name = extract_repository_name(
    str(request.repository_url)
)

    repository = repository_service.create(
        user_id=current_user.id,
        repository_name=repository_name,
        repository_url=request.repository_url,
    )

    return repository


@router.get(
    "/",
    response_model=list[RepositoryResponse],
)
async def list_repositories(
    current_user=Depends(
        get_current_user
    ),
):

    return repository_service.list(
        current_user.id
    )


@router.delete(
    "/{repository_id}",
)
async def delete_repository(
    repository_id: str,
    current_user=Depends(
        get_current_user
    ),
):

    repository = repository_service.get(
        repository_id
    )

    if repository.user_id != current_user.id:

        raise HTTPException(
            status_code=403,
            detail="Forbidden",
        )

    repository_cleanup_service.delete_repository(
        repository_id
    )

    return {
        "message": "Repository deleted successfully."
    }