from app.Core.Utils.QueryRequest import QuerySpecification, SortOption
from app.Infrastructure.Database.QuerySpecificationBuilder import (
    SpecificationBuilder,
)
from app.Infrastructure.Database.Schema.UserSchema import UserSchema


class UserSpecification:
    SortableFields = {
        "id": UserSchema.id,
        "email": UserSchema.email,
        "name": UserSchema.name,
        "role": UserSchema.role,
    }

    Builder = SpecificationBuilder(
        UserSchema,
        sortable_columns=SortableFields,
        searchable_columns=[UserSchema.email, UserSchema.name],
        filter_builders={"role": lambda value: UserSchema.role == value},
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
