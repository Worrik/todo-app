from abc import abstractmethod
from typing import Protocol


class NotificationService(Protocol):
    @abstractmethod
    async def send_notification(self, destination: str, message: str) -> None:
        raise NotImplementedError
