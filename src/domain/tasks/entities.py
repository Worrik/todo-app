from dataclasses import dataclass


@dataclass
class TaskAssigneeDM:
    id: int
    name: str
    email: str


@dataclass
class TaskExecutorDM:
    id: int
    name: str
    email: str


@dataclass
class TaskStatusDM:
    id: int
    name: str


@dataclass
class TaskPriorityDM:
    id: int
    name: str
    value: int


@dataclass
class TaskDM:
    id: int
    title: str
    description: str
    assignee: TaskAssigneeDM | None = None
    executors: list[TaskExecutorDM] | None = None
    status: TaskStatusDM | None = None
    priority: TaskPriorityDM | None = None
