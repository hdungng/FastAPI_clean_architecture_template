from fastapi import APIRouter, Depends

from app.Core.CurrentUser import CurrentUser
from app.Core.Response import ResponseFactory
from app.Modules.Auth.JwtAuthorize import Authorize
from app.Modules.Users.Dto.CreateUserRequestDTO import CreateUserRequestDTO
from app.Modules.Users.Dto.UpdateUserRequestDTO import UpdateUserRequestDTO

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


@router.get("")
async def GetAll(
    _: CurrentUser = Depends(Authorize(Role="Admin")),
    service: IUserService = Depends(GetUserService),
):
    users = await service.GetAll()
    return ResponseFactory.Ok(users)


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


@router.put("/{id}")
async def Update(
    id: int,
    request: UpdateUserRequestDTO,
    _: CurrentUser = Depends(Authorize(Role="Admin")),
    service: IUserService = Depends(GetUserService),
):
    user = await service.Update(id, request)
    return ResponseFactory.Ok(user)


@router.delete("/{id}")
async def Delete(
    id: int,
    _: CurrentUser = Depends(Authorize(Role="Admin")),
    service: IUserService = Depends(GetUserService),
):
    await service.Delete(id)
    return ResponseFactory.Ok(message="User deleted")
