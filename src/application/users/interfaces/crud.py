from abc import abstractmethod
from typing import Protocol


class UserUpdate(Protocol):
    @abstractmethod
    async def update(
        self, user_id: int, name: str, email: str, password: str
    ) -> None: ...
