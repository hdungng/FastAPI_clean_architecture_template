from pydantic import BaseModel, EmailStr


class CreateUserRequestDTO(BaseModel):
    email: EmailStr
    name: str
    password: str
