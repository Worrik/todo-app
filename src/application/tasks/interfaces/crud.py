from abc import abstractmethod
from typing import Protocol

from src.application.common.pagination.dto import PaginationDTO
from src.application.tasks.dto import (
    DeleteTaskDTO,
    DeleteTaskPriorityDTO,
    DeleteTaskStatusDTO,
    GetTaskDTO,
    NewTaskDTO,
    NewTaskPriorityDTO,
    NewTaskStatusDTO,
    UpdateTaskDTO,
)
from src.domain.tasks.entities import TaskDM, TaskPriorityDM, TaskStatusDM


class TaskCreate(Protocol):
    @abstractmethod
    async def create(self, dto: NewTaskDTO) -> int: ...


class TaskGet(Protocol):
    @abstractmethod
    async def get(self, dto: GetTaskDTO) -> TaskDM: ...

    @abstractmethod
    async def get_all(self) -> list[TaskDM]: ...

    @abstractmethod
    async def get_paginated(self, pagination: PaginationDTO) -> list[TaskDM]: ...


class TaskUpdate(Protocol):
    @abstractmethod
    async def update(self, dto: UpdateTaskDTO) -> None: ...

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


class TaskDelete(Protocol):
    @abstractmethod
    async def delete(self, dto: DeleteTaskDTO) -> None: ...


class TaskStatusCreate(Protocol):
    @abstractmethod
    async def create(self, dto: NewTaskStatusDTO) -> int: ...


class TaskStatusGet(Protocol):
    @abstractmethod
    async def get_all(self) -> list[TaskStatusDM]: ...


class TaskStatusDelete(Protocol):
    @abstractmethod
    async def delete(self, dto: DeleteTaskStatusDTO) -> None: ...


class TaskPriorityCreate(Protocol):
    @abstractmethod
    async def create(self, dto: NewTaskPriorityDTO) -> int: ...


class TaskPriorityGet(Protocol):
    @abstractmethod
    async def get_all(self) -> list[TaskPriorityDM]: ...


class TaskPriorityDelete(Protocol):
    @abstractmethod
    async def delete(self, dto: DeleteTaskPriorityDTO) -> None: ...
