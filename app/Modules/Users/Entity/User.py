from dataclasses import dataclass

@dataclass
class User:
    Id: int | None
    Email: str
    Name: str
    HashedPassword: str
    Role: str
