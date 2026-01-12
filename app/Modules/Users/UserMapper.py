from .Dto.CreateUserRequestDTO import CreateUserRequestDTO
from .Dto.UpdateUserRequestDTO import UpdateUserRequestDTO
from .Dto.UserResponseDTO import UserResponseDTO
from .Entity.User import User


class UserMapper:

    @staticmethod
    def ToEntity(dto: CreateUserRequestDTO) -> User:
        return User(
            id=None,
            email=dto.email,
            name=dto.name,
            hashed_password="",
        )

    @staticmethod
    def ApplyUpdates(user: User, dto: UpdateUserRequestDTO) -> User:
        if dto.email is not None:
            user.email = dto.email
        if dto.name is not None:
            user.name = dto.name
        if dto.password is not None:
            user.hashed_password = dto.password
        if dto.role is not None:
            user.role = dto.role
        return user

    @staticmethod
    def ToResponse(user: User) -> UserResponseDTO:
        return UserResponseDTO(
            id=user.id,
            email=user.email,
            name=user.name or "",
            role=user.role,
        )

    @staticmethod
    def ToResponseList(users: list[User]) -> list[UserResponseDTO]:
        return [UserMapper.ToResponse(user) for user in users]

    @staticmethod
    def FromEntity(model: User) -> User:
        return model
