from sqlalchemy import delete, select

from app.Core.Utils.QueryRequest import Pageable, QuerySpecification
from app.Infrastructure.Database.BaseRepository import BaseRepository
from .Entity.User import User
from .IUserRepository import IUserRepository
from .UserMapper import UserMapper
from .UserSpecification import UserSpecification


class UserRepository(BaseRepository, IUserRepository):
    def __init__(self, Db):
        super().__init__(Db)

    async def Create(self, user: User) -> User:
        self.Db.add(user)
        await self.Db.flush()
        await self.Db.refresh(user)
        return UserMapper.FromEntity(user)

    async def GetById(self, id: int) -> User:
        stmt = select(User).where(User.id == id)
        result = await self.Db.execute(stmt)
        model = result.scalar_one()

        return UserMapper.FromEntity(model)

    async def GetByEmail(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self.Db.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            return None

        return UserMapper.FromEntity(model)

    async def GetAll(
        self, spec: QuerySpecification, pageable: Pageable
    ) -> tuple[list[User], int]:
        base_query, count_query = UserSpecification.Build(spec, pageable)

        total_result = await self.Db.execute(count_query)
        total = total_result.scalar_one()

        result = await self.Db.execute(base_query)
        models = result.scalars().all()

        return [UserMapper.FromEntity(model) for model in models], total

    async def Update(self, user: User) -> User:
        await self.Db.flush()
        await self.Db.refresh(user)
        return UserMapper.FromEntity(user)

    async def Delete(self, id: int) -> None:
        stmt = delete(User).where(User.id == id)
        await self.Db.execute(stmt)
