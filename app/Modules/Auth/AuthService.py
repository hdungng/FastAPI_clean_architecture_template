from datetime import datetime, timedelta
import jwt

from app.Config.Settings import Settings
from app.Core.IUnitOfWork import IUnitOfWork
from app.Modules.Users.IUserRepository import IUserRepository
from app.Core.Utils.CrytoUtil import CryptoUtil
from app.Core.AppException import AppException
from .Dto.AuthDTO import LoginRequest, RegisterRequest, TokenResponse
from .AuthMapper import AuthMapper


class AuthService:

    def __init__(
        self,
        userRepo: IUserRepository,
        unitOfWork: IUnitOfWork,
        settings: Settings,
    ):
        self.UserRepo = userRepo
        self.UnitOfWork = unitOfWork
        self.Settings = settings

    def _GenerateAccessToken(self, user_id: int, role: str) -> str:
        payload = {
            "sub": user_id,
            "role": role,
            "exp": datetime.utcnow() + timedelta(minutes=self.Settings.jwt_expire_minutes),
        }
        return jwt.encode(
            payload,
            self.Settings.jwt_secret,
            algorithm="HS256",
        )

    async def Login(self, dto: LoginRequest) -> TokenResponse:
        user = await self.UserRepo.GetByEmail(dto.Email)
        if not user or not CryptoUtil.VerifyPassword(dto.Password, user.HashedPassword):
            raise AppException("Invalid credentials")

        return TokenResponse(
            AccessToken=self._GenerateAccessToken(user.Id, user.Role),
        )

    async def Register(self, dto: RegisterRequest) -> TokenResponse:
        existed = await self.UserRepo.GetByEmail(dto.Email)
        if existed:
            raise AppException("Email already exists")

        user = AuthMapper.CreateUser(
            email=dto.Email,
            name=dto.Name,
            hashed_password=CryptoUtil.HashPassword(dto.Password),
        )

        user = await self.UserRepo.Create(user)
        await self.UnitOfWork.Commit()

        return TokenResponse(
            AccessToken=self._GenerateAccessToken(user.Id, user.Role),
        )
