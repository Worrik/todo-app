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
from src.application.tasks.interfaces.crud import (
    TaskCreate,
    TaskDelete,
    TaskGet,
    TaskPriorityCreate,
    TaskPriorityDelete,
    TaskPriorityGet,
    TaskStatusCreate,
    TaskStatusDelete,
    TaskStatusGet,
    TaskUpdate,
)
from src.application.tasks.interfaces.repo import TaskRepo
from src.domain.tasks.entities import TaskDM, TaskPriorityDM, TaskStatusDM


class TaskGateway(TaskGet, TaskCreate, TaskUpdate, TaskDelete):
    def __init__(self, task_repo: TaskRepo) -> None:
        self._task_repo = task_repo

    async def create(self, dto: NewTaskDTO) -> int:
        executors_ids = set(dto.executors_ids or [])
        return await self._task_repo.create(
            title=dto.title,
            description=dto.description,
            assignee_id=dto.assignee_id,
            executors_ids=executors_ids,
            status_id=dto.status_id,
            priority_id=dto.priority_id,
        )

    async def get(self, dto: GetTaskDTO) -> TaskDM:
        return await self._task_repo.get(dto.id)

    async def get_all(self) -> list[TaskDM]:
        return await self._task_repo.get_all()

    async def get_paginated(self, pagination: PaginationDTO) -> list[TaskDM]:
        return await self._task_repo.get_paginated(pagination.offset, pagination.limit)

    async def update(self, dto: UpdateTaskDTO) -> None:
        await self._task_repo.update(
            task_id=dto.id,
            title=dto.title,
            desctiption=dto.description,
            assignee_id=dto.assignee_id,
            status_id=dto.status_id,
            priority_id=dto.priority_id,
        )

    async def delete(self, dto: DeleteTaskDTO) -> None:
        await self._task_repo.delete(dto.id)

    async def assign_executor(self, task_id: int, executor_id: int) -> None:
        await self._task_repo.assign_executor(task_id, executor_id)

    async def unassign_executor(self, task_id: int, executor_id: int) -> None:
        await self._task_repo.unassign_executor(task_id, executor_id)

    async def assign_executors(self, task_id: int, executors_ids: list[int]) -> None:
        await self._task_repo.assign_executors(task_id, executors_ids)

    async def unassign_executors(self, task_id: int) -> None:
        await self._task_repo.unassign_executors(task_id)

    async def change_status(self, task_id: int, status_id: int) -> None:
        await self._task_repo.change_status(task_id, status_id)

    async def change_priority(self, task_id: int, priority_id: int) -> None:
        await self._task_repo.change_priority(task_id, priority_id)

    async def assign_assignee(self, task_id: int, assignee_id: int) -> None:
        await self._task_repo.assign_assignee(task_id, assignee_id)

    async def unassign_assignee(self, task_id: int) -> None:
        await self._task_repo.unassign_assignee(task_id)


class TaskStatusGateway(TaskStatusCreate, TaskStatusGet, TaskStatusDelete):
    def __init__(self, task_repo: TaskRepo) -> None:
        self._task_repo = task_repo

    async def create(self, dto: NewTaskStatusDTO) -> int:
        return await self._task_repo.create_status(dto.name)

    async def get_all(self) -> list[TaskStatusDM]:
        return await self._task_repo.get_statuses()

    async def delete(self, dto: DeleteTaskStatusDTO) -> None:
        return await self._task_repo.delete_status(dto.id)


class TaskPriorityGateway(TaskPriorityCreate, TaskPriorityGet, TaskPriorityDelete):
    def __init__(self, task_repo: TaskRepo) -> None:
        self._task_repo = task_repo

    async def create(self, dto: NewTaskPriorityDTO) -> int:
        return await self._task_repo.create_priority(name=dto.name, value=dto.value)

    async def get_all(self) -> list[TaskPriorityDM]:
        return await self._task_repo.get_priorities()

    async def delete(self, dto: DeleteTaskPriorityDTO) -> None:
        return await self._task_repo.delete_priority(dto.id)
