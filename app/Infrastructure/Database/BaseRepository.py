from sqlalchemy.ext.asyncio import AsyncSession

class BaseRepository:

    def __init__(self, Db: AsyncSession):
        self.Db = Db
