from typing import Protocol

class IUnitOfWork(Protocol):

    async def Commit(self) -> None:
        ...

    async def Rollback(self) -> None:
        ...
