from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.Infrastructure.Database.Base import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column("user_id", ForeignKey("users.id"), index=True)
    token: Mapped[str] = mapped_column("token", String(255), unique=True, index=True)
    expires_at: Mapped[datetime] = mapped_column("expires_at", DateTime(timezone=True))
    is_revoked: Mapped[bool] = mapped_column("is_revoked", default=False, server_default="false")
