from pydantic import BaseModel, EmailStr


class CreateUserRequestDTO(BaseModel):
    Email: EmailStr
    Name: str
    Password: str
