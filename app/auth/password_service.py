from passlib.context import CryptContext


class PasswordService:

    def __init__(self):

        self.context = CryptContext(
            schemes=["argon2"],
            deprecated="auto",
        )

    def hash_password(
        self,
        password: str,
    ) -> str:

        return self.context.hash(password)

    def verify_password(
        self,
        plain_password: str,
        password_hash: str,
    ) -> bool:

        return self.context.verify(
            plain_password,
            password_hash,
        )