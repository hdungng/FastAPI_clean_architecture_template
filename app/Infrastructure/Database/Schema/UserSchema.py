from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.Infrastructure.Database.Base import Base

class UserSchema(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    Role: Mapped[str] = mapped_column(String(50), default="User")
    hashed_password: Mapped[str] = mapped_column(String(255))
