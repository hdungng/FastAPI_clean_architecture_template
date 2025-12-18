from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.Infrastructure.Database.Session import GetDb
from .UserRepository import UserRepository
from .UserService import UserService, IUserService


def GetUserService(
    Db: AsyncSession = Depends(GetDb),
) -> IUserService:
    repo = UserRepository(Db)
    return UserService(repo)
