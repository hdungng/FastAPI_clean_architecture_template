from typing import Protocol
from .Entity.User import User

class IUserRepository(Protocol):

    async def Create(self, user: User) -> User:
        ...

    async def GetById(self, id: int):
        ...

    async def GetByEmail(self, email: str) -> User | None:
        ...

    async def GetAll(self) -> list[User]:
        ...

    async def Update(self, user: User) -> User:
        ...

    async def Delete(self, id: int) -> None:
        ...
