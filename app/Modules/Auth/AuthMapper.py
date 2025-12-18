from datetime import datetime, timedelta
from app.Modules.Users.Entity.User import User
from app.Modules.Auth.Entity.RefreshToken import RefreshToken
from app.Core.Utils.StringUtil import StringUtil
from app.Core.Utils.DateTimeUtil import DateTimeUtil


class AuthMapper:

    @staticmethod
    def CreateUser(email: str, hashed_password: str) -> User:
        return User(
            Email=email,
            HashedPassword=hashed_password,
            Role="User",
            CreatedAt=DateTimeUtil.UtcNow(),
        )

    @staticmethod
    def CreateRefreshToken(user_id: int) -> RefreshToken:
        return RefreshToken(
            UserId=user_id,
            Token=StringUtil.RandomToken(),
            ExpiresAt=DateTimeUtil.AfterDays(7),
        )
