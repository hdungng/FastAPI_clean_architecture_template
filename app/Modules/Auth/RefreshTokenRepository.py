from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .IRefreshTokenRepository import IRefreshTokenRepository
from .Entity.RefreshToken import RefreshToken


class RefreshTokenRepository(IRefreshTokenRepository):

    def __init__(self, Db: AsyncSession):
        self.Db = Db

    async def Create(self, token: RefreshToken) -> RefreshToken:
        self.Db.add(token)
        await self.Db.flush()
        await self.Db.refresh(token)
        return token

    async def GetByToken(self, token: str):
        stmt = select(RefreshToken).where(
            RefreshToken.Token == token,
            RefreshToken.IsRevoked == False,
        )

        result = await self.Db.execute(stmt)
        model = result.scalar_one_or_none()

        if not model:
            return None

        return model

    async def Revoke(self, token: RefreshToken) -> None:
        token.IsRevoked = True
        await self.Db.flush()
        await self.Db.refresh(token)
