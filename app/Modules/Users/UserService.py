from app.Core.AppException import AppException
from app.Core.CurrentUser import CurrentUser
from app.Core.IUnitOfWork import IUnitOfWork
from app.Core.Utils.CrytoUtil import CryptoUtil
from .Dto.CreateUserRequestDTO import CreateUserRequestDTO
from .Dto.UpdateUserRequestDTO import UpdateUserRequestDTO
from .Dto.UserResponseDTO import UserResponseDTO
from .IUserRepository import IUserRepository
from .UserMapper import UserMapper


class IUserService:
    async def Create(self, dto: CreateUserRequestDTO) -> UserResponseDTO: ...
    async def GetMe(self, current: CurrentUser) -> UserResponseDTO: ...
    async def GetById(self, user_id: int) -> UserResponseDTO: ...
    async def GetAll(self) -> list[UserResponseDTO]: ...
    async def Update(self, user_id: int, dto: UpdateUserRequestDTO) -> UserResponseDTO: ...
    async def Delete(self, user_id: int) -> None: ...


class UserService:

    def __init__(
        self,
        repository: IUserRepository,
        unitOfWork: IUnitOfWork,
    ):
        self.Repository = repository
        self.UnitOfWork = unitOfWork

    async def Create(self, dto: CreateUserRequestDTO) -> UserResponseDTO:
        try:
            existed = await self.Repository.GetByEmail(dto.Email)
            if existed:
                raise AppException("Email already exists")

            user = UserMapper.ToEntity(dto)
            user.HashedPassword = CryptoUtil.HashPassword(dto.Password)

            saved = await self.Repository.Create(user)
            await self.UnitOfWork.Commit()

            return UserMapper.ToResponse(saved)

        except Exception:
            await self.UnitOfWork.Rollback()
            raise

    async def GetMe(self, current: CurrentUser) -> UserResponseDTO:
        user = await self.Repository.GetById(current.Id)
        return UserMapper.ToResponse(user)

    async def GetById(self, user_id: int) -> UserResponseDTO:
        user = await self.Repository.GetById(user_id)
        return UserMapper.ToResponse(user)

    async def GetAll(self) -> list[UserResponseDTO]:
        users = await self.Repository.GetAll()
        return UserMapper.ToResponseList(users)

    async def Update(self, user_id: int, dto: UpdateUserRequestDTO) -> UserResponseDTO:
        try:
            user = await self.Repository.GetById(user_id)

            if dto.Email:
                existing = await self.Repository.GetByEmail(dto.Email)
                if existing and existing.Id != user_id:
                    raise AppException("Email already exists")

            updated_user = UserMapper.ApplyUpdates(user, dto)

            if dto.Password:
                updated_user.HashedPassword = CryptoUtil.HashPassword(dto.Password)

            saved = await self.Repository.Update(updated_user)
            await self.UnitOfWork.Commit()

            return UserMapper.ToResponse(saved)

        except Exception:
            await self.UnitOfWork.Rollback()
            raise

    async def Delete(self, user_id: int) -> None:
        try:
            await self.Repository.GetById(user_id)
            await self.Repository.Delete(user_id)
            await self.UnitOfWork.Commit()
        except Exception:
            await self.UnitOfWork.Rollback()
            raise
