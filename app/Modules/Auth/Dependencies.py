from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.Infrastructure.Database.Session import GetDb
from app.Infrastructure.Database.UnitOfWork import UnitOfWork
from app.Config.Settings import get_settings

from app.Modules.Users.UserRepository import UserRepository
from .RefreshTokenRepository import RefreshTokenRepository
from .AuthService import AuthService


def GetAuthService(
    db: AsyncSession = Depends(GetDb),
    settings = Depends(get_settings),
):
    user_repo = UserRepository(db)
    refresh_repo = RefreshTokenRepository(db)
    unitOfWork = UnitOfWork(db)

    return AuthService(
        user_repo,
        refresh_repo,
        unitOfWork,
        settings,
    )
