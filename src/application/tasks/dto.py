from dataclasses import dataclass

from src.application.common.pagination.constants import Empty


@dataclass
class NewTaskDTO:
    title: str
    description: str
    assignee_id: int | None = None
    executors_ids: list[int] | None = None
    status_id: int | None = None
    priority_id: int | None = None


@dataclass
class UpdateTaskDTO:
    id: int
    title: str | Empty = Empty.UNSET
    description: str | Empty = Empty.UNSET
    assignee_id: int | None | Empty = Empty.UNSET
    executors_ids: list[int] | Empty = Empty.UNSET
    status_id: int | None | Empty = Empty.UNSET
    priority_id: int | None | Empty = Empty.UNSET


@dataclass
class DeleteTaskDTO:
    id: int


@dataclass
class GetTaskDTO:
    id: int


@dataclass
class NewTaskStatusDTO:
    name: str


@dataclass
class DeleteTaskStatusDTO:
    id: int


@dataclass
class NewTaskPriorityDTO:
    name: str
    value: int


@dataclass
class DeleteTaskPriorityDTO:
    id: int


@dataclass
class SendTaskStatusUpdateDTO:
    id: int
