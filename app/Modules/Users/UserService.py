from .UserMapper import UserMapper
from .IUserRepository import IUserRepository
from .Dto import CreateUserRequestDTO, UserResponseDTO
from app.Core.IUnitOfWork import IUnitOfWork
from app.Core.CurrentUser import CurrentUser

class IUserService:
    async def CreateUser(self, dto: CreateUserRequestDTO) -> UserResponseDTO: ...
    async def GetMe(self, current: CurrentUser) -> UserResponseDTO: ...


class UserService:

    def __init__(
        self,
        repository: IUserRepository,
        unitOfWork: IUnitOfWork,
    ):
        self.Repository = repository
        self.UnitOfWork = unitOfWork

    async def CreateUser(self, dto: CreateUserRequestDTO) -> UserResponseDTO:
        try:
            user = UserMapper.ToEntity(dto)
            user.HashedPassword = f"hashed-{dto.Password}"

            saved = await self.Repository.Create(user)
            await self.UnitOfWork.Commit()

            return UserMapper.ToResponse(saved)

        except Exception:
            await self.UnitOfWork.Rollback()
            raise

    async def GetMe(self, current: CurrentUser) -> UserResponseDTO:
        user = await self.Repository.GetById(current.Id)
        return UserMapper.ToResponse(user)
