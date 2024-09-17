from typing import Self

from pydantic import BaseModel

from src.domain.tasks.entities import TaskPriorityDM


class NewTaskPrioritySchema(BaseModel):
    name: str
    value: int


class TaskPrioritySchema(BaseModel):
    id: int
    name: str
    value: int

    @classmethod
    def from_domain_model(cls, task_priority_dm: TaskPriorityDM) -> Self:
        return cls(
            id=task_priority_dm.id,
            name=task_priority_dm.name,
            value=task_priority_dm.value,
        )
