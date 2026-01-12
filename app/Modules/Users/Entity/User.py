from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.Infrastructure.Database.Base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column("id", primary_key=True, index=True)
    email: Mapped[str] = mapped_column("email", String(255), unique=True, index=True)
    name: Mapped[str | None] = mapped_column("name", String(255))
    role: Mapped[str] = mapped_column("role", String(50), default="User")
    hashed_password: Mapped[str] = mapped_column("hashed_password", String(255))
