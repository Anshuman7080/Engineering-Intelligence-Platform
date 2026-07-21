from datetime import datetime, timedelta, UTC

from jose import jwt
from jose.exceptions import JWTError

from app.core.settings import settings


class JWTService:

    def create_access_token(
        self,
        user_id: str,
    ) -> str:

        expire = datetime.now(
            UTC
        ) + timedelta(
            minutes=settings.JWT_EXPIRE_MINUTES
        )

        payload = {
            "sub": user_id,
            "exp": expire,
        }

        return jwt.encode(
            payload,
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM,
        )

    def verify_access_token(
        self,
        token: str,
    ) -> str | None:

        try:

            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=[
                    settings.JWT_ALGORITHM
                ],
            )

            return payload.get("sub")

        except JWTError:

            return None