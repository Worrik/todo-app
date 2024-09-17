from dataclasses import dataclass
from typing import Generic, Self, TypeVar

Item = TypeVar("Item")


@dataclass(frozen=True)
class PaginationDTO:
    offset: int | None = None
    limit: int | None = None


@dataclass(frozen=True)
class PaginationResultDTO:
    offset: int | None
    limit: int | None
    total: int

    @classmethod
    def from_pagination(cls, pagination: PaginationDTO, total: int) -> Self:
        return cls(
            offset=pagination.offset,
            limit=pagination.limit,
            total=total,
        )


@dataclass(frozen=True)
class PaginatedItemsDTO(Generic[Item]):
    data: list[Item]
    pagination: PaginationResultDTO
