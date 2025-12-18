from typing import Any, Callable, Iterable, Mapping

from sqlalchemy import asc, desc, func, or_, select

from app.Core.Utils.QueryRequest import Pageable, QuerySpecification


class SqlAlchemySpecificationBuilder:
    def __init__(
        self,
        model,
        *,
        sortable_columns: Mapping[str, Any],
        searchable_columns: Iterable[Any] | None = None,
        filter_builders: Mapping[str, Callable[[Any], Any]] | None = None,
    ):
        self.Model = model
        self.SortableColumns = sortable_columns
        self.SearchableColumns = list(searchable_columns or [])
        self.FilterBuilders = filter_builders or {}
        self.DefaultSortColumn = next(iter(sortable_columns.values()))

    def Build(self, spec: QuerySpecification, pageable: Pageable):
        base_query = select(self.Model)
        count_query = select(func.count()).select_from(self.Model)
        filters = []

        if spec.Search and self.SearchableColumns:
            pattern = f"%{spec.Search}%"
            filters.append(or_(*[column.ilike(pattern) for column in self.SearchableColumns]))

        for key, value in (spec.Filters or {}).items():
            if value is None:
                continue
            builder = self.FilterBuilders.get(key)
            if builder:
                filters.append(builder(value))

        if filters:
            base_query = base_query.where(*filters)
            count_query = count_query.where(*filters)

        sort_column = self.SortableColumns.get(spec.Sort.Field, self.DefaultSortColumn)
        order_by = desc(sort_column) if spec.Sort.Direction == "desc" else asc(sort_column)

        base_query = base_query.order_by(order_by).offset(pageable.Offset).limit(pageable.PageSize)

        return base_query, count_query
