from dataclasses import dataclass
from typing import Any, Mapping

from app.Core.AppException import AppException
from app.Core.Utils.PaginationUtil import PaginationUtil


@dataclass
class SortOption:
    Field: str
    Direction: str

    @staticmethod
    def Create(sort_by: str, sort_direction: str, allowed_fields: set[str]) -> "SortOption":
        field = (sort_by or "").lower()
        if field not in allowed_fields:
            raise AppException("Invalid sort field")

        direction = (sort_direction or "").lower()
        if direction not in {"asc", "desc"}:
            raise AppException("Invalid sort direction")

        return SortOption(Field=field, Direction=direction)


@dataclass
class Pageable:
    Page: int
    PageSize: int
    Offset: int

    @staticmethod
    def Create(page: int, page_size: int) -> "Pageable":
        normalized_page, normalized_size, offset = PaginationUtil.Normalize(page, page_size)
        return Pageable(Page=normalized_page, PageSize=normalized_size, Offset=offset)


@dataclass
class QuerySpecification:
    Search: str | None
    Filters: Mapping[str, Any] | None
    Sort: SortOption
