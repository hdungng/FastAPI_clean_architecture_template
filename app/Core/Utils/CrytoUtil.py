from passlib.context import CryptContext

_pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

class CryptoUtil:

    @staticmethod
    def HashPassword(password: str) -> str:
        return _pwd_context.hash(password)

    @staticmethod
    def VerifyPassword(password: str, hashed: str) -> bool:
        return _pwd_context.verify(password, hashed)
