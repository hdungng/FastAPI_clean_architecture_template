from datetime import datetime, timedelta
import jwt

from app.Config.Settings import Settings
from app.Core.IUnitOfWork import IUnitOfWork
from app.Modules.Users.UserRepository import IUserRepository
from app.Core.Utils.CrytoUtil import CryptoUtil
from app.Core.AppException import AppException
from .IRefreshTokenRepository import IRefreshTokenRepository
from .Dto.AuthDTO import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    RefreshTokenRequest,
)
from .AuthMapper import AuthMapper


class AuthService:

    def __init__(
        self,
        userRepo: IUserRepository,
        refreshTokenRepo: IRefreshTokenRepository,
        unitOfWork: IUnitOfWork,
        settings: Settings,
    ):
        self.UserRepo = userRepo
        self.RefreshTokenRepo = refreshTokenRepo
        self.UnitOfWork = unitOfWork
        self.Settings = settings

    def _GenerateAccessToken(self, user_id: int, role: str) -> str:
        payload = {
            "sub": user_id,
            "role": role,
            "exp": datetime.utcnow() + timedelta(minutes=15),
        }
        return jwt.encode(
            payload,
            self.Settings.jwt_secret,
            algorithm="HS256",
        )

    async def Login(self, dto: LoginRequest) -> TokenResponse:
        user = await self.UserRepo.GetByEmail(dto.Email)
        if not user or user.HashedPassword != f"hashed-{dto.Password}":
            raise AppException("Invalid credentials")

        refresh = AuthMapper.CreateRefreshToken(user.Id)

        await self.RefreshTokenRepo.Create(refresh)
        await self.UnitOfWork.Commit()

        return TokenResponse(
            AccessToken=self._GenerateAccessToken(user.Id),
            RefreshToken=refresh.Token,
        )

    async def Refresh(self, dto: RefreshTokenRequest) -> TokenResponse:
        token = await self.RefreshTokenRepo.GetByToken(dto.RefreshToken)

        if not token or token.ExpiresAt < datetime.utcnow():
            raise Exception("Invalid refresh token")

        await self.RefreshTokenRepo.Revoke(token)

        new_refresh = AuthMapper.CreateRefreshToken(token.UserId)
        await self.RefreshTokenRepo.Create(new_refresh)

        await self.UnitOfWork.Commit()

        return TokenResponse(
            AccessToken=self._GenerateAccessToken(token.UserId, token.Role),
            RefreshToken=new_refresh.Token,
        )

    def _GenerateAccessToken(self, user_id: int, role: str) -> str:
        payload = {
            "sub": user_id,
            "role": role,
            "exp": datetime.utcnow() + timedelta(minutes=15),
        }
        return jwt.encode(
            payload,
            self.Settings.jwt_secret,
            algorithm="HS256",
        )

    async def Register(self, dto: RegisterRequest) -> TokenResponse:
        # 1. Check email exists
        existed = await self.UserRepo.GetByEmail(dto.Email)
        if existed:
            raise AppException("Email already exists")

        # 2. Create user entity
        user = AuthMapper.CreateUser(
            email=dto.Email,
            hashed_password=CryptoUtil.HashPassword(dto.Password),
        )

        # 3. Save user
        await self.UserRepo.Create(user)

        # 4. Create refresh token
        refresh = AuthMapper.CreateRefreshToken(user.Id)
        await self.RefreshTokenRepo.Create(refresh)

        # 5. Commit transaction
        await self.UnitOfWork.Commit()

        # 6. Return token
        return TokenResponse(
            AccessToken=self._GenerateAccessToken(user.Id, user.Role),
            RefreshToken=refresh.Token,
        )
