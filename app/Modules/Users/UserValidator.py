from app.Core.AppException import AppException
from .Dto.CreateUserRequestDTO import CreateUserRequestDTO
from .Dto.UpdateUserRequestDTO import UpdateUserRequestDTO


class UserValidator:
    _ALLOWED_ROLES = {"User", "Admin"}

    @staticmethod
    def ValidateCreate(dto: CreateUserRequestDTO) -> None:
        UserValidator._validate_name(dto.name)
        UserValidator._validate_password(dto.password)

    @staticmethod
    def ValidateUpdate(dto: UpdateUserRequestDTO) -> None:
        if dto.name is not None:
            UserValidator._validate_name(dto.name)
        if dto.password is not None:
            UserValidator._validate_password(dto.password)
        if dto.role is not None and dto.role not in UserValidator._ALLOWED_ROLES:
            raise AppException("Role must be one of: Admin, User")

    @staticmethod
    def _validate_name(name: str) -> None:
        if not name or not name.strip():
            raise AppException("Name is required")
        if len(name.strip()) < 2:
            raise AppException("Name must be at least 2 characters long")

    @staticmethod
    def _validate_password(password: str) -> None:
        if len(password) < 8:
            raise AppException("Password must be at least 8 characters long")
        if password.isalpha() or password.isnumeric():
            raise AppException("Password must include both letters and numbers")
