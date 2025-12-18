from sqlalchemy.ext.asyncio import AsyncSession
from app.Core.IUnitOfWork import IUnitOfWork

class UnitOfWork(IUnitOfWork):

    def __init__(self, Db: AsyncSession):
        self.Db = Db

    async def Commit(self) -> None:
        await self.Db.commit()

    async def Rollback(self) -> None:
        await self.Db.rollback()
