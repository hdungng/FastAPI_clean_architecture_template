from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.Infrastructure.Database.Session import GetDb, GetReadOnlyDb
from app.Infrastructure.Database.UnitOfWork import UnitOfWork
from .UserRepository import UserRepository
from .UserService import UserService, IUserService


def GetUserService(
    Db: AsyncSession = Depends(GetDb),
) -> IUserService:
    repo = UserRepository(Db)
    unit_of_work = UnitOfWork(Db)
    return UserService(repo, unit_of_work)


def GetReadOnlyUserService(
    Db: AsyncSession = Depends(GetReadOnlyDb),
) -> IUserService:
    repo = UserRepository(Db)
    unit_of_work = UnitOfWork(Db)
    return UserService(repo, unit_of_work)
