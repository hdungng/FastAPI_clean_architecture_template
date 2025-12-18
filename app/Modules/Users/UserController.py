from fastapi import APIRouter, Depends, Query

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
    page: int = Query(1, ge=1, alias="Page"),
    page_size: int = Query(10, ge=1, le=100, alias="PageSize"),
    search: str | None = Query(None, alias="Search"),
    role: str | None = Query(None, alias="Role"),
    sort_by: str = Query("id", alias="SortBy"),
    sort_direction: str = Query("asc", alias="SortDirection"),
):
    users = await service.GetAll(
        page=page,
        page_size=page_size,
        search=search,
        role=role,
        sort_by=sort_by,
        sort_direction=sort_direction,
    )
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
