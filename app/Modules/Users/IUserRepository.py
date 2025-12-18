from typing import Protocol
from .Entity.User import User

class IUserRepository(Protocol):

    async def Create(self, user: User) -> User:
        ...

    async def GetById(self, id: int):
        ...