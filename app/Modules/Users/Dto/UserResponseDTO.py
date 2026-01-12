from pydantic import BaseModel, EmailStr


class UserResponseDTO(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
