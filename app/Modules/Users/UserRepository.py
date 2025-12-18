from sqlalchemy import insert, select
from app.Infrastructure.Database.BaseRepository import BaseRepository
from .UserRepository import IUserRepository
from .Entity.User import User
from app.Infrastructure.Database.Schema.UserSchema import UserSchema


class UserRepository(BaseRepository, IUserRepository):

    async def Create(self, user: User) -> User:
        stmt = (
            insert(UserSchema)
            .values(email=user.Email, hashed_password=user.HashedPassword)
            .returning(UserSchema)
        )

        result = await self.Db.execute(stmt)
        model = result.scalar_one()

        return User(
            Id=model.id, Email=model.email, HashedPassword=model.hashed_password
        )

    async def GetById(self, id: int):
        stmt = select(UserSchema).where(UserSchema.id == id)
        result = await self.Db.execute(stmt)
        model = result.scalar_one()

        return User(
            Id=model.id,
            Email=model.email,
            HashedPassword=model.hashed_password,
    )
