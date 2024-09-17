from typing import Self

from pydantic import BaseModel

from src.domain.tasks.entities import TaskStatusDM


class NewTaskStatusSchema(BaseModel):
    name: str


class TaskStatusSchema(BaseModel):
    id: int
    name: str

    @classmethod
    def from_domain_model(cls, task_status_dm: TaskStatusDM) -> Self:
        return cls(
            id=task_status_dm.id,
            name=task_status_dm.name,
        )
