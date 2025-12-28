from app.Core.Utils.QueryRequest import QuerySpecification, SortOption
from app.Infrastructure.Database.QuerySpecificationBuilder import (
    SpecificationBuilder,
)
from app.Modules.Users.Entity.User import User


class UserSpecification:
    SortableFields = {
        "id": User.Id,
        "email": User.Email,
        "name": User.Name,
        "role": User.Role,
    }

    Builder = SpecificationBuilder(
        User,
        sortable_columns=SortableFields,
        searchable_columns=[User.Email, User.Name],
        filter_builders={"role": lambda value: User.Role == value},
    )

    @staticmethod
    def CreateSort(sort_by: str, sort_direction: str) -> SortOption:
        return SortOption.Create(sort_by, sort_direction, set(UserSpecification.SortableFields))

    @staticmethod
    def Create(search: str | None, role: str | None, sort: SortOption) -> QuerySpecification:
        return QuerySpecification(Search=search, Filters={"role": role}, Sort=sort)

    @staticmethod
    def Build(spec: QuerySpecification, pageable):
        return UserSpecification.Builder.Build(spec, pageable)
