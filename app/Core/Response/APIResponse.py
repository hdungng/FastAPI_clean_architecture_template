from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    Success: bool
    Data: Optional[T] = None
    Message: Optional[str] = None


class PagedResult(BaseModel):
    Items: list
    Total: int
    Page: int
    PageSize: int
