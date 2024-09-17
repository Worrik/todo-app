from abc import abstractmethod
from typing import Protocol

from src.application.common.pagination.constants import Empty
from src.domain.users.entities import UserDM


class UserRepo(Protocol):
    @abstractmethod
    async def create(
        self, name: str, email: str, password: str, is_active: bool = True
    ) -> int: ...

    @abstractmethod
    async def get(self, user_id: int) -> UserDM: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> UserDM: ...

    @abstractmethod
    async def update(
        self,
        user_id: int,
        name: str | Empty = Empty.UNSET,
        email: str | Empty = Empty.UNSET,
        password: str | Empty = Empty.UNSET,
        is_active: bool | Empty = Empty.UNSET,
    ) -> None: ...

    @abstractmethod
    async def delete(self, user_id: int) -> None: ...
