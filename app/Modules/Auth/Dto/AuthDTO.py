from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    Email: EmailStr
    Password: str


class TokenResponse(BaseModel):
    AccessToken: str
    RefreshToken: str
    TokenType: str = "bearer"


class RefreshTokenRequest(BaseModel):
    RefreshToken: str


class RegisterRequest(BaseModel):
    Email: EmailStr
    Name: str
    Password: str