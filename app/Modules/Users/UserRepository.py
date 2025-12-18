from sqlalchemy import delete, insert, select, update

from app.Core.Utils.QueryRequest import Pageable, QuerySpecification
from app.Infrastructure.Database.BaseRepository import BaseRepository
from app.Infrastructure.Database.Schema.UserSchema import UserSchema
from .Entity.User import User
from .IUserRepository import IUserRepository
from .UserMapper import UserMapper
from .UserSpecification import UserSpecification


class UserRepository(BaseRepository, IUserRepository):
    def __init__(self, Db):
        super().__init__(Db)

    async def Create(self, user: User) -> User:
        stmt = insert(UserSchema).values(**UserMapper.ToCreateValues(user)).returning(UserSchema)

        result = await self.Db.execute(stmt)
        model = result.scalar_one()

        return UserMapper.FromSchema(model)

    async def GetById(self, id: int) -> User:
        stmt = select(UserSchema).where(UserSchema.id == id)
        result = await self.Db.execute(stmt)
        model = result.scalar_one()

        return UserMapper.FromSchema(model)

    async def GetByEmail(self, email: str) -> User | None:
        stmt = select(UserSchema).where(UserSchema.email == email)
        result = await self.Db.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            return None

        return UserMapper.FromSchema(model)

    async def GetAll(
        self, spec: QuerySpecification, pageable: Pageable
    ) -> tuple[list[User], int]:
        base_query, count_query = UserSpecification.Build(spec, pageable)

        total_result = await self.Db.execute(count_query)
        total = total_result.scalar_one()

        result = await self.Db.execute(base_query)
        models = result.scalars().all()

        return [UserMapper.FromSchema(model) for model in models], total

    async def Update(self, user: User) -> User:
        stmt = (
            update(UserSchema)
            .where(UserSchema.id == user.Id)
            .values(**UserMapper.ToUpdateValues(user))
            .returning(UserSchema)
        )

        result = await self.Db.execute(stmt)
        model = result.scalar_one()

        return UserMapper.FromSchema(model)

    async def Delete(self, id: int) -> None:
        stmt = delete(UserSchema).where(UserSchema.id == id)
        await self.Db.execute(stmt)
