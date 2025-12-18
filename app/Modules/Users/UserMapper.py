from .Dto import CreateUserRequestDTO, UserResponseDTO
from .Entity.User import User

class UserMapper:

    @staticmethod
    def ToEntity(dto: CreateUserRequestDTO) -> User:
        return User(
            Id=None,
            Email=dto.Email,
            HashedPassword=""
        )

    @staticmethod
    def ToResponse(user: User) -> UserResponseDTO:
        return UserResponseDTO(
            Id=user.Id,
            Email=user.Email
        )
