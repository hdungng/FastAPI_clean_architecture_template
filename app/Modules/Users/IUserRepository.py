from typing import Protocol

from app.Core.Utils.QueryRequest import Pageable, QuerySpecification
from .Entity.User import User


class IUserRepository(Protocol):

    async def Create(self, user: User) -> User:
        ...

    async def GetById(self, id: int):
        ...

    async def GetByEmail(self, email: str) -> User | None:
        ...

    async def GetAll(
        self, spec: QuerySpecification, pageable: Pageable
    ) -> tuple[list[User], int]:
        ...

    async def Update(self, user: User) -> User:
        ...

    async def Delete(self, id: int) -> None:
        ...
