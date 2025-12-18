import secrets
import re

class StringUtil:

    @staticmethod
    def RandomToken(length: int = 64) -> str:
        return secrets.token_urlsafe(length)

    @staticmethod
    def NormalizeEmail(email: str) -> str:
        return email.strip().lower()

    @staticmethod
    def IsStrongPassword(password: str) -> bool:
        return (
            len(password) >= 8
            and re.search(r"[A-Z]", password)
            and re.search(r"[a-z]", password)
            and re.search(r"\d", password)
        )
