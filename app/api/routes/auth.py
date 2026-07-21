from fastapi import APIRouter, Depends

from app.api.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    AuthResponse,
    UserResponse,
)

from app.api.dependencies.auth import (
    get_current_user,
)

from app.auth.auth_service import AuthService

router = APIRouter()

auth_service = AuthService()


@router.post(
    "/register",
    response_model=AuthResponse,
)
async def register(
    request: RegisterRequest,
):

    return auth_service.register(
        username=request.username,
        email=request.email,
        password=request.password,
    )


@router.post(
    "/login",
    response_model=AuthResponse,
)
async def login(
    request: LoginRequest,
):

    return auth_service.login(
        email=request.email,
        password=request.password,
    )


@router.get(
    "/me",
    response_model=UserResponse,
)
async def me(
    current_user=Depends(
        get_current_user
    ),
):

    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
    )