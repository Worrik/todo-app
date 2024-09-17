from src.application.common.messaging.interfaces import StatusUpdateMessagePublisher
from src.application.common.notifications.interfaces import NotificationService
from src.application.common.pagination.constants import Empty
from src.application.common.pagination.dto import PaginationDTO
from src.application.tasks.dto import (
    DeleteTaskDTO,
    DeleteTaskPriorityDTO,
    DeleteTaskStatusDTO,
    GetTaskDTO,
    NewTaskDTO,
    NewTaskPriorityDTO,
    NewTaskStatusDTO,
    SendTaskStatusUpdateDTO,
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
from src.domain.tasks.entities import TaskDM, TaskPriorityDM, TaskStatusDM


class GetTaskInteractor:
    def __init__(self, task_gateway: TaskGet) -> None:
        self._task_gateway = task_gateway

    async def __call__(self, dto: GetTaskDTO) -> TaskDM:
        return await self._task_gateway.get(dto)


class GetPaginatedTasksInteractor:
    def __init__(self, task_gateway: TaskGet) -> None:
        self._task_gateway = task_gateway

    async def __call__(self, dto: PaginationDTO) -> list[TaskDM]:
        return await self._task_gateway.get_paginated(dto)


class CreateTaskInteractor:
    def __init__(self, task_gateway: TaskCreate) -> None:
        self._task_gateway = task_gateway

    async def __call__(self, dto: NewTaskDTO) -> int:
        return await self._task_gateway.create(dto)


class UpdateTaskInteractor:
    def __init__(
        self, task_gateway: TaskUpdate, publisher: StatusUpdateMessagePublisher
    ) -> None:
        self._task_gateway = task_gateway
        self._publisher = publisher

    async def __call__(self, dto: UpdateTaskDTO) -> None:
        await self._task_gateway.update(dto)
        if dto.status_id is not Empty.UNSET:
            await self.send_status_update(dto.id)

    async def send_status_update(self, task_id: int) -> None:
        await self._publisher.publish({"task_id": task_id})


class DeleteTaskInteractor:
    def __init__(self, task_gateway: TaskDelete) -> None:
        self._task_gateway = task_gateway

    async def __call__(self, dto: DeleteTaskDTO) -> None:
        await self._task_gateway.delete(dto)


class CreateTaskStatusInteractor:
    def __init__(self, status_gateway: TaskStatusCreate) -> None:
        self._status_gateway = status_gateway

    async def __call__(self, dto: NewTaskStatusDTO) -> int:
        return await self._status_gateway.create(dto)


class GetTaskStatusesInteractor:
    def __init__(self, status_gateway: TaskStatusGet) -> None:
        self._status_gateway = status_gateway

    async def __call__(self) -> list[TaskStatusDM]:
        return await self._status_gateway.get_all()


class DeleteTaskStatusInteractor:
    def __init__(self, status_gateway: TaskStatusDelete) -> None:
        self._status_gateway = status_gateway

    async def __call__(self, dto: DeleteTaskStatusDTO) -> None:
        await self._status_gateway.delete(dto)


class CreateTaskPriorityInteractor:
    def __init__(self, priority_gateway: TaskPriorityCreate) -> None:
        self._priority_gateway = priority_gateway

    async def __call__(self, dto: NewTaskPriorityDTO) -> int:
        return await self._priority_gateway.create(dto)


class GetTaskPrioritiesInteractor:
    def __init__(self, priority_gateway: TaskPriorityGet) -> None:
        self._priority_gateway = priority_gateway

    async def __call__(self) -> list[TaskPriorityDM]:
        return await self._priority_gateway.get_all()


class DeleteTaskPriorityInteractor:
    def __init__(self, priority_gateway: TaskPriorityDelete) -> None:
        self._priority_gateway = priority_gateway

    async def __call__(self, dto: DeleteTaskPriorityDTO) -> None:
        await self._priority_gateway.delete(dto)


class SendTaskStatusUpdateInteractor:
    def __init__(
        self, task_gateway: TaskGet, notification_service: NotificationService
    ) -> None:
        self._task_gateway = task_gateway
        self._notification_service = notification_service

    async def __call__(self, dto: SendTaskStatusUpdateDTO) -> None:
        task = await self._task_gateway.get(GetTaskDTO(id=dto.id))
        await self.send_notification(task)

    async def send_notification(self, task: TaskDM) -> None:
        if not task.assignee:
            return

        new_status = task.status.name if task.status else "Empty"
        message = f'Task "{task.title}" status was updated to "{new_status}"'
        await self._notification_service.send_notification(
            task.assignee.email,
            message,
        )
