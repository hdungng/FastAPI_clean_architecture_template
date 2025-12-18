from pydantic import BaseModel, EmailStr


class UserResponseDTO(BaseModel):
    Id: int
    Name: str
    Email: EmailStr
    Role: str
