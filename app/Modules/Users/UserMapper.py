from app.Infrastructure.Database.Schema.UserSchema import UserSchema
from .Dto.CreateUserRequestDTO import CreateUserRequestDTO
from .Dto.UpdateUserRequestDTO import UpdateUserRequestDTO
from .Dto.UserResponseDTO import UserResponseDTO
from .Entity.User import User


class UserMapper:

    @staticmethod
    def ToEntity(dto: CreateUserRequestDTO) -> User:
        return User(
            Id=None,
            Email=dto.Email,
            Name=dto.Name,
            HashedPassword="",
        )

    @staticmethod
    def ApplyUpdates(user: User, dto: UpdateUserRequestDTO) -> User:
        if dto.Email is not None:
            user.Email = dto.Email
        if dto.Name is not None:
            user.Name = dto.Name
        if dto.Password is not None:
            user.HashedPassword = dto.Password
        if dto.Role is not None:
            user.Role = dto.Role
        return user

    @staticmethod
    def ToResponse(user: User) -> UserResponseDTO:
        return UserResponseDTO(
            Id=user.Id,
            Email=user.Email,
            Name=user.Name or "",
            Role=user.Role,
        )

    @staticmethod
    def ToResponseList(users: list[User]) -> list[UserResponseDTO]:
        return [UserMapper.ToResponse(user) for user in users]

    @staticmethod
    def FromSchema(model: UserSchema) -> User:
        return User(
            Id=model.id,
            Email=model.email,
            Name=model.name,
            HashedPassword=model.hashed_password,
            Role=model.role,
        )

    @staticmethod
    def ToCreateValues(user: User) -> dict:
        return {
            "email": user.Email,
            "name": user.Name,
            "role": user.Role,
            "hashed_password": user.HashedPassword,
        }

    @staticmethod
    def ToUpdateValues(user: User) -> dict:
        return {
            "email": user.Email,
            "name": user.Name,
            "role": user.Role,
            "hashed_password": user.HashedPassword,
        }
