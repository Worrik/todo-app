from abc import abstractmethod
from typing import Protocol

from src.application.common.pagination.constants import Empty
from src.domain.tasks.entities import TaskDM, TaskPriorityDM, TaskStatusDM


class TaskRepo(Protocol):
    @abstractmethod
    async def create(
        self,
        title: str,
        description: str,
        assignee_id: int | None = None,
        status_id: int | None = None,
        priority_id: int | None = None,
        executors_ids: set[int] | None = None,
    ) -> int: ...

    @abstractmethod
    async def get(self, id: int) -> TaskDM: ...

    @abstractmethod
    async def get_all(self) -> list[TaskDM]: ...

    @abstractmethod
    async def get_paginated(
        self, offset: int | None, limit: int | None
    ) -> list[TaskDM]: ...

    @abstractmethod
    async def update(
        self,
        task_id: int,
        title: str | Empty = Empty.UNSET,
        desctiption: str | Empty = Empty.UNSET,
        assignee_id: int | None | Empty = Empty.UNSET,
        status_id: int | None | Empty = Empty.UNSET,
        priority_id: int | None | Empty = Empty.UNSET,
    ) -> None: ...

    @abstractmethod
    async def delete(self, task_id: int) -> None: ...

    @abstractmethod
    async def assign_executor(self, task_id: int, executor_id: int) -> None: ...

    @abstractmethod
    async def unassign_executor(self, task_id: int, executor_id: int) -> None: ...

    @abstractmethod
    async def assign_executors(
        self, task_id: int, executors_ids: list[int]
    ) -> None: ...

    @abstractmethod
    async def unassign_executors(self, task_id: int) -> None: ...

    @abstractmethod
    async def change_status(self, task_id: int, status_id: int) -> None: ...

    @abstractmethod
    async def change_priority(self, task_id: int, priority_id: int) -> None: ...

    @abstractmethod
    async def assign_assignee(self, task_id: int, assignee_id: int) -> None: ...

    @abstractmethod
    async def unassign_assignee(self, task_id: int) -> None: ...

    @abstractmethod
    async def create_status(self, name: str) -> int: ...

    @abstractmethod
    async def get_statuses(self) -> list[TaskStatusDM]: ...

    @abstractmethod
    async def delete_status(self, status_id: int) -> None: ...

    @abstractmethod
    async def create_priority(self, name: str, value: int) -> int: ...

    @abstractmethod
    async def get_priorities(self) -> list[TaskPriorityDM]: ...

    @abstractmethod
    async def delete_priority(self, priority_id: int) -> None: ...
