from typing import Any, Generic, Optional, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    message: Optional[str] = None
    meta: dict[str, Any] = Field(default_factory=dict)


class PagedResult(BaseModel):
    items: list
    total: int
    page: int
    page_size: int
