from fastapi import APIRouter, Depends

from app.Core import CurrentUser
from app.Core.Response import ResponseFactory
from app.Modules.Auth.JwtAuthorize import Authorize

from .Dto.AuthDTO import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
)
from .Dependencies import GetAuthQueryService, GetAuthService
from .AuthService import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
async def Login(
    request: LoginRequest,
    service: AuthService = Depends(GetAuthQueryService),
):
    token = await service.Login(request)
    return ResponseFactory.Ok(token)


@router.post("/register")
async def Register(
    request: RegisterRequest,
    service: AuthService = Depends(GetAuthService),
):
    token = await service.Register(request)
    return ResponseFactory.Created(token)


@router.get("/me")
async def GetMe(
    current: CurrentUser = Depends(Authorize()),
):
    return ResponseFactory.Ok(current)


@router.post("/logout")
async def Logout(
    _: CurrentUser = Depends(Authorize()),
):
    return ResponseFactory.Ok(message="Logged out")
