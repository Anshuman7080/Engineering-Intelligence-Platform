from sqlalchemy import select

from app.database.session import SessionLocal
from app.auth.models import User


class UserRepository:

    def create_user(
        self,
        username: str,
        email: str,
        password_hash: str,
    ) -> User:

        with SessionLocal() as session:

            user = User(
                username=username,
                email=email,
                password_hash=password_hash,
            )

            session.add(user)
            session.commit()
            session.refresh(user)

            return user

    def get_by_email(
        self,
        email: str,
    ) -> User | None:

        with SessionLocal() as session:

            return session.execute(
                select(User).where(
                    User.email == email
                )
            ).scalar_one_or_none()

    def get_by_username(
        self,
        username: str,
    ) -> User | None:

        with SessionLocal() as session:

            return session.execute(
                select(User).where(
                    User.username == username
                )
            ).scalar_one_or_none()

    def get_by_id(
        self,
        user_id: str,
    ) -> User | None:

        with SessionLocal() as session:

            return session.get(
                User,
                user_id,
            )