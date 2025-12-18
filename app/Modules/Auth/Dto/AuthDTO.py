from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    Email: EmailStr
    Password: str


class TokenResponse(BaseModel):
    AccessToken: str
    TokenType: str = "bearer"


class RegisterRequest(BaseModel):
    Email: EmailStr
    Name: str
    Password: str
