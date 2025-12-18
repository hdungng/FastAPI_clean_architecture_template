from fastapi import APIRouter, Depends

from app.Core import CurrentUser
from app.Core.Response import ResponseFactory
from app.Modules.Auth.JwtAuthorize import Authorize

from .Dto.AuthDTO import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    RefreshTokenRequest,
)
from .Dependencies import GetAuthService
from .AuthService import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
async def Login(
    request: LoginRequest,
    service: AuthService = Depends(GetAuthService),
):
    token = await service.Login(request)
    return ResponseFactory.Ok(token)


@router.post("/register")
async def Register(
    request: RegisterRequest,
    service: AuthService = Depends(GetAuthService),
):
    user = await service.Register(request)
    return ResponseFactory.Created(user)


@router.get("/me")
async def GetMe(
    current: CurrentUser = Depends(Authorize()),
):
    return ResponseFactory.Ok(current)


@router.post("/logout")
async def Logout(
    _: CurrentUser = Depends(Authorize()),
):
    # Nếu dùng blacklist / redis → gọi service
    return ResponseFactory.Ok(message="Logged out")