from abc import abstractmethod
from typing import Any, Protocol


class StatusUpdateMessagePublisher(Protocol):
    @abstractmethod
    async def publish(self, message: Any) -> None: ...
