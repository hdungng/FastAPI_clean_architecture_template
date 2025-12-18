from sqlalchemy import insert, select
from app.Infrastructure.Database.BaseRepository import BaseRepository
from .IUserRepository import IUserRepository
from .Entity.User import User
from app.Infrastructure.Database.Schema.UserSchema import UserSchema


class UserRepository(BaseRepository, IUserRepository):

    async def Create(self, user: User) -> User:
        stmt = (
            insert(UserSchema)
            .values(
                email=user.Email,
                name=user.Name,
                role=user.Role,
                hashed_password=user.HashedPassword,
            )
            .returning(UserSchema)
        )

        result = await self.Db.execute(stmt)
        model = result.scalar_one()

        return User(
            Id=model.id,
            Email=model.email,
            Name=model.name,
            HashedPassword=model.hashed_password,
            Role=model.role,
        )

    async def GetById(self, id: int) -> User:
        stmt = select(UserSchema).where(UserSchema.id == id)
        result = await self.Db.execute(stmt)
        model = result.scalar_one()

        return User(
            Id=model.id,
            Email=model.email,
            Name=model.name,
            HashedPassword=model.hashed_password,
            Role=model.role,
        )

    async def GetByEmail(self, email: str) -> User | None:
        stmt = select(UserSchema).where(UserSchema.email == email)
        result = await self.Db.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            return None

        return User(
            Id=model.id,
            Email=model.email,
            Name=model.name,
            HashedPassword=model.hashed_password,
            Role=model.role,
        )
