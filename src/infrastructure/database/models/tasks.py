from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.models.base import Base, TimestampMixin


class Task(Base, TimestampMixin):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    assignee_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    status_id: Mapped[int | None] = mapped_column(ForeignKey("statuses.id"))
    priority_id: Mapped[int | None] = mapped_column(ForeignKey("priorities.id"))

    assignee = relationship("User")
    executors = relationship("User", secondary="executors")
    status = relationship("TaskStatus")
    priority = relationship("TaskPriority")


class TaskExecutor(Base, TimestampMixin):
    __tablename__ = "executors"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), primary_key=True)


class TaskStatus(Base, TimestampMixin):
    __tablename__ = "statuses"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)


class TaskPriority(Base, TimestampMixin):
    __tablename__ = "priorities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    value: Mapped[int] = mapped_column(nullable=False)
