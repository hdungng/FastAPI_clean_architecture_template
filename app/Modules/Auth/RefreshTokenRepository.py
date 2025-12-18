from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .RefreshTokenRepository import IRefreshTokenRepository
from .Entity.RefreshToken import RefreshToken
from app.Infrastructure.Database.Schema.RefreshTokenSchema import RefreshTokenSchema


class RefreshTokenRepository(IRefreshTokenRepository):

    def __init__(self, Db: AsyncSession):
        self.Db = Db

    async def Create(self, token: RefreshToken) -> RefreshToken:
        stmt = (
            insert(RefreshTokenSchema)
            .values(
                user_id=token.UserId,
                token=token.Token,
                expires_at=token.ExpiresAt,
                is_revoked=False,
            )
            .returning(RefreshTokenSchema)
        )

        result = await self.Db.execute(stmt)
        model = result.scalar_one()

        return RefreshToken(
            Id=model.id,
            UserId=model.user_id,
            Token=model.token,
            ExpiresAt=model.expires_at,
            IsRevoked=model.is_revoked,
        )

    async def GetByToken(self, token: str):
        stmt = select(RefreshTokenSchema).where(
            RefreshTokenSchema.token == token,
            RefreshTokenSchema.is_revoked == False,
        )

        result = await self.Db.execute(stmt)
        model = result.scalar_one_or_none()

        if not model:
            return None

        return RefreshToken(
            Id=model.id,
            UserId=model.user_id,
            Token=model.token,
            ExpiresAt=model.expires_at,
            IsRevoked=model.is_revoked,
        )

    async def Revoke(self, token: RefreshToken) -> None:
        stmt = (
            update(RefreshTokenSchema)
            .where(RefreshTokenSchema.id == token.Id)
            .values(is_revoked=True)
        )
        await self.Db.execute(stmt)
