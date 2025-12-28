from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.Infrastructure.Database.Base import Base


class User(Base):
    __tablename__ = "users"

    Id: Mapped[int] = mapped_column("id", primary_key=True, index=True)
    Email: Mapped[str] = mapped_column("email", String(255), unique=True, index=True)
    Name: Mapped[str | None] = mapped_column("name", String(255))
    Role: Mapped[str] = mapped_column("role", String(50), default="User")
    HashedPassword: Mapped[str] = mapped_column("hashed_password", String(255))
