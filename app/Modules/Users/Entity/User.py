from dataclasses import dataclass

@dataclass
class User:
    Id: int | None
    Email: str
    Name: str | None = None
    HashedPassword: str = ""
    Role: str = "User"
