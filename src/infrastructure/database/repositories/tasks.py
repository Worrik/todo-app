import sqlalchemy as sa

from src.application.common.pagination.constants import Empty
from src.application.tasks.interfaces.repo import TaskRepo
from src.domain.tasks.entities import TaskDM, TaskPriorityDM, TaskStatusDM
from src.infrastructure.database.converters import convert_task_model_to_domain_model
from src.infrastructure.database.models.tasks import (
    Task,
    TaskExecutor,
    TaskPriority,
    TaskStatus,
)
from src.infrastructure.database.repositories.base import SQLAlchemyRepo


class TaskRepoImpl(SQLAlchemyRepo, TaskRepo):
    _joined_loads = [
        sa.orm.joinedload(Task.assignee),
        sa.orm.joinedload(Task.status),
        sa.orm.joinedload(Task.priority),
        sa.orm.joinedload(Task.executors),
    ]

    @staticmethod
    def _map_to_domain_model(model: Task) -> TaskDM:
        return convert_task_model_to_domain_model(model)

    async def get(self, id: int) -> TaskDM:
        query = (
            sa.select(Task).where(Task.id == id).options(*self._joined_loads).limit(1)
        )
        result = await self._session.execute(query)
        task = result.scalars().first()
        if not task:
            raise ValueError(f"Task with id {id} not found")
        return self._map_to_domain_model(task)

    async def get_all(self) -> list[TaskDM]:
        query = sa.select(Task).options(*self._joined_loads)
        result = await self._session.execute(query)
        return [self._map_to_domain_model(task) for task in result.unique().scalars()]

    async def get_paginated(self, offset: int, limit: int) -> list[TaskDM]:
        query = sa.select(Task).options(*self._joined_loads).offset(offset).limit(limit)
        result = await self._session.execute(query)
        return [self._map_to_domain_model(task) for task in result.unique().scalars()]

    async def create(
        self,
        title: str,
        description: str,
        assignee_id: int | None = None,
        status_id: int | None = None,
        priority_id: int | None = None,
        executors_ids: set[int] | None = None,
    ) -> int:
        task = Task(
            title=title,
            description=description,
            assignee_id=assignee_id,
            status_id=status_id,
            priority_id=priority_id,
        )
        self._session.add(task)
        await self._session.commit()
        for executor_id in executors_ids or []:
            self._session.add(TaskExecutor(user_id=executor_id, task_id=task.id))
        await self._session.commit()
        return task.id

    async def update(
        self,
        task_id: int,
        title: str | Empty = Empty.UNSET,
        desctiption: str | Empty = Empty.UNSET,
        assignee_id: int | None | Empty = Empty.UNSET,
        status_id: int | None | Empty = Empty.UNSET,
        priority_id: int | None | Empty = Empty.UNSET,
    ) -> None:
        query = sa.update(Task).where(Task.id == task_id)
        if title is not Empty.UNSET:
            query = query.values(title=title)
        if desctiption is not Empty.UNSET:
            query = query.values(description=desctiption)
        if assignee_id is not Empty.UNSET:
            query = query.values(assignee_id=assignee_id)
        if status_id is not Empty.UNSET:
            query = query.values(status_id=status_id)
        if priority_id is not Empty.UNSET:
            query = query.values(priority_id=priority_id)
        await self._session.execute(query)
        await self._session.commit()

    async def delete(self, task_id: int) -> None:
        query = sa.delete(Task).where(Task.id == task_id)
        await self._session.execute(query)
        await self._session.commit()

    async def assign_executor(self, task_id: int, executor_id: int) -> None:
        self._session.add(TaskExecutor(user_id=executor_id, task_id=task_id))
        await self._session.commit()

    async def unassign_executor(self, task_id: int, executor_id: int) -> None:
        query = sa.delete(TaskExecutor).where(
            sa.and_(
                TaskExecutor.task_id == task_id, TaskExecutor.user_id == executor_id
            )
        )
        await self._session.execute(query)
        await self._session.commit()

    async def assign_executors(self, task_id: int, executors_ids: list[int]) -> None:
        for executor_id in executors_ids:
            self._session.add(TaskExecutor(user_id=executor_id, task_id=task_id))
        await self._session.commit()

    async def unassign_executors(self, task_id: int) -> None:
        query = sa.delete(TaskExecutor).where(TaskExecutor.task_id == task_id)
        await self._session.execute(query)
        await self._session.commit()

    async def change_status(self, task_id: int, status_id: int) -> None:
        query = sa.update(Task).where(Task.id == task_id).values(status_id=status_id)
        await self._session.execute(query)
        await self._session.commit()

    async def change_priority(self, task_id: int, priority_id: int) -> None:
        query = (
            sa.update(Task).where(Task.id == task_id).values(priority_id=priority_id)
        )
        await self._session.execute(query)
        await self._session.commit()

    async def assign_assignee(self, task_id: int, assignee_id: int) -> None:
        query = (
            sa.update(Task).where(Task.id == task_id).values(assignee_id=assignee_id)
        )
        await self._session.execute(query)
        await self._session.commit()

    async def unassign_assignee(self, task_id: int) -> None:
        query = sa.update(Task).where(Task.id == task_id).values(assignee_id=None)
        await self._session.execute(query)
        await self._session.commit()

    async def create_status(self, name: str) -> int:
        status = TaskStatus(name=name)
        self._session.add(status)
        await self._session.commit()
        return status.id

    async def get_statuses(self) -> list[TaskStatusDM]:
        query = sa.select(TaskStatus)
        result = await self._session.execute(query)
        return [
            TaskStatusDM(id=status.id, name=status.name) for status in result.scalars()
        ]

    async def delete_status(self, status_id: int) -> None:
        query = sa.delete(TaskStatus).where(TaskStatus.id == status_id)
        await self._session.execute(query)
        await self._session.commit()

    async def create_priority(self, name: str, value: int) -> int:
        priority = TaskPriority(name=name, value=value)
        self._session.add(priority)
        await self._session.commit()
        return priority.id

    async def get_priorities(self) -> list[TaskPriorityDM]:
        query = sa.select(TaskPriority)
        result = await self._session.execute(query)
        return [
            TaskPriorityDM(id=priority.id, name=priority.name, value=priority.value)
            for priority in result.scalars()
        ]

    async def delete_priority(self, priority_id: int) -> None:
        query = sa.delete(TaskPriority).where(TaskPriority.id == priority_id)
        await self._session.execute(query)
        await self._session.commit()
