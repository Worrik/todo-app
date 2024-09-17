from typing import Self

from pydantic import BaseModel

from src.application.common.pagination.constants import Empty
from src.controllers.api.tasks.priorities.schemas import TaskPrioritySchema
from src.controllers.api.tasks.statuses.schemas import TaskStatusSchema
from src.domain.tasks.entities import TaskDM


class NewTaskSchema(BaseModel):
    title: str
    description: str
    assignee_id: int | None = None
    executors_ids: list[int] | None = None
    status_id: int | None = None
    priority_id: int | None = None


class UpdateTaskSchema(BaseModel):
    title: str | Empty = Empty.UNSET
    description: str | Empty = Empty.UNSET
    assignee_id: int | None | Empty = Empty.UNSET
    executors_ids: list[int] | Empty = Empty.UNSET
    status_id: int | None | Empty = Empty.UNSET
    priority_id: int | None | Empty = Empty.UNSET


class TaskAssigneeSchema(BaseModel):
    id: int
    name: str
    email: str


class TaskExecutorSchema(BaseModel):
    id: int
    name: str
    email: str


class TaskSchema(BaseModel):
    id: int
    title: str
    description: str
    assignee: TaskAssigneeSchema | None = None
    executors: list[TaskExecutorSchema] | None = None
    status: TaskStatusSchema | None = None
    priority: TaskPrioritySchema | None = None

    @classmethod
    def from_domain_model(cls, task_dm: TaskDM) -> Self:
        assignee = (
            TaskAssigneeSchema(
                id=task_dm.assignee.id,
                name=task_dm.assignee.name,
                email=task_dm.assignee.email,
            )
            if task_dm.assignee
            else None
        )
        executors = [
            TaskExecutorSchema(
                id=executor.id,
                name=executor.name,
                email=executor.email,
            )
            for executor in task_dm.executors or []
        ]
        status = (
            TaskStatusSchema(
                id=task_dm.status.id,
                name=task_dm.status.name,
            )
            if task_dm.status
            else None
        )
        priority = (
            TaskPrioritySchema(
                id=task_dm.priority.id,
                name=task_dm.priority.name,
                value=task_dm.priority.value,
            )
            if task_dm.priority
            else None
        )
        return cls(
            id=task_dm.id,
            title=task_dm.title,
            description=task_dm.description,
            assignee=assignee,
            executors=executors,
            status=status,
            priority=priority,
        )
