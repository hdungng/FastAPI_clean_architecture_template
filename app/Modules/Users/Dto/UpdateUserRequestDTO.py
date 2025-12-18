from typing import Optional
from pydantic import BaseModel, EmailStr


class UpdateUserRequestDTO(BaseModel):
    Email: Optional[EmailStr] = None
    Name: Optional[str] = None
    Password: Optional[str] = None
    Role: Optional[str] = None
