from typing import Protocol
from .Entity.RefreshToken import RefreshToken

class IRefreshTokenRepository(Protocol):

    async def Create(self, token: RefreshToken) -> RefreshToken:
        ...

    async def GetByToken(self, token: str) -> RefreshToken | None:
        ...

    async def Revoke(self, token: RefreshToken) -> None:
        ...
