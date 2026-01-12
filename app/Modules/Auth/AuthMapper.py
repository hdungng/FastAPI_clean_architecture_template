from app.Modules.Users.Entity.User import User


class AuthMapper:

    @staticmethod
    def CreateUser(email: str, name: str, hashed_password: str) -> User:
        return User(
            id=None,
            email=email,
            name=name,
            hashed_password=hashed_password,
            role="User",
        )
