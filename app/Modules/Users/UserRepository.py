from sqlalchemy import delete, insert, select, update
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

    async def GetAll(self) -> list[User]:
        stmt = select(UserSchema)
        result = await self.Db.execute(stmt)
        return [
            User(
                Id=model.id,
                Email=model.email,
                Name=model.name,
                HashedPassword=model.hashed_password,
                Role=model.role,
            )
            for model in result.scalars().all()
        ]

    async def Update(self, user: User) -> User:
        stmt = (
            update(UserSchema)
            .where(UserSchema.id == user.Id)
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

    async def Delete(self, id: int) -> None:
        stmt = delete(UserSchema).where(UserSchema.id == id)
        await self.Db.execute(stmt)
