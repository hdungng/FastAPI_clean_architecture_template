from dataclasses import dataclass
from datetime import datetime

@dataclass
class RefreshToken:
    Id: int | None
    UserId: int
    Token: str
    ExpiresAt: datetime
    IsRevoked: bool
