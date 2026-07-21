from fastapi import HTTPException, status

from app.auth.repository import UserRepository
from app.auth.password_service import PasswordService
from app.auth.jwt_service import JWTService


class AuthService:

    def __init__(self):

        self.user_repository = UserRepository()
        self.password_service = PasswordService()
        self.jwt_service = JWTService()

    def register(
        self,
        username: str,
        email: str,
        password: str,
    ):

        if self.user_repository.get_by_username(username):

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists.",
            )

        if self.user_repository.get_by_email(email):

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists.",
            )

        password_hash = self.password_service.hash_password(
            password
        )

        user = self.user_repository.create_user(
            username=username,
            email=email,
            password_hash=password_hash,
        )

        token = self.jwt_service.create_access_token(
            user.id
        )

        return {
            "access_token": token,
        }

    def login(
        self,
        email: str,
        password: str,
    ):

        user = self.user_repository.get_by_email(
            email
        )

        if user is None:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        valid = self.password_service.verify_password(
            password,
            user.password_hash,
        )

        if not valid:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        token = self.jwt_service.create_access_token(
            user.id
        )

        return {
            "access_token": token,
        }

    def get_current_user(
        self,
        user_id: str,
    ):

        user = self.user_repository.get_by_id(
            user_id
        )

        if user is None:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found.",
            )

        return user