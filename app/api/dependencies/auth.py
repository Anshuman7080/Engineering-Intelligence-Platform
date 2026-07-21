from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer

from app.auth.auth_service import AuthService
from app.auth.jwt_service import JWTService

security = HTTPBearer()

jwt_service = JWTService()

auth_service = AuthService()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
):

    token = credentials.credentials

    user_id = jwt_service.verify_access_token(
        token
    )

    if user_id is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token.",
        )

    return auth_service.get_current_user(
        user_id
    )