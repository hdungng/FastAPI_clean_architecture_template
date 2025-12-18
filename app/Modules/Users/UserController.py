from fastapi import APIRouter, Depends

from app.Core.CurrentUser import CurrentUser
from app.Core.Response import ResponseFactory
from app.Modules.Auth.JwtAuthorize import Authorize
from app.Modules.Users.Dto.CreateUserRequestDTO import CreateUserRequestDTO
from app.Modules.Users.Dto.UserResponseDTO import UserResponseDTO

from .UserService import IUserService
from .Dependencies import GetUserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("")
async def Create(
    request: CreateUserRequestDTO,
    service: IUserService = Depends(GetUserService),
):
    user = await service.Create(request)
    return ResponseFactory.Created(user)


@router.get("/me")
async def GetMe(
    current: CurrentUser = Depends(Authorize()),
    service: IUserService = Depends(GetUserService),
):
    user = await service.GetMe(current)
    return ResponseFactory.Ok(user)



@router.get("/{id}")
async def GetById(
    id: int,
    _: CurrentUser = Depends(Authorize(Role="Admin")),
    service: IUserService = Depends(GetUserService),
):
    user = await service.GetById(id)
    return ResponseFactory.Ok(user)
