from typing import Optional
from pydantic import BaseModel, EmailStr


class UpdateUserRequestDTO(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
