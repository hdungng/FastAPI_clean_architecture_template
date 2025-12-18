from app.Modules.Users.Entity.User import User


class AuthMapper:

    @staticmethod
    def CreateUser(email: str, name: str, hashed_password: str) -> User:
        return User(
            Id=None,
            Email=email,
            Name=name,
            HashedPassword=hashed_password,
            Role="User",
        )
