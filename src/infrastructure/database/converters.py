from src.domain.tasks.entities import (
    TaskAssigneeDM,
    TaskDM,
    TaskExecutorDM,
    TaskPriorityDM,
    TaskStatusDM,
)
from src.domain.users.entities import UserDM
from src.infrastructure.database.models.tasks import Task
from src.infrastructure.database.models.users import User


def convert_task_model_to_domain_model(model: Task) -> TaskDM:
    assignee = (
        TaskAssigneeDM(
            id=model.assignee.id,
            name=model.assignee.name,
            email=model.assignee.email,
        )
        if model.assignee
        else None
    )
    executors = [
        TaskExecutorDM(
            id=executor.id,
            name=executor.name,
            email=executor.email,
        )
        for executor in model.executors
    ]
    status = (
        TaskStatusDM(
            id=model.status.id,
            name=model.status.name,
        )
        if model.status
        else None
    )
    priority = (
        TaskPriorityDM(
            id=model.priority.id,
            name=model.priority.name,
            value=model.priority.value,
        )
        if model.priority
        else None
    )
    return TaskDM(
        id=model.id,
        title=model.title,
        description=model.description,
        assignee=assignee,
        executors=executors,
        status=status,
        priority=priority,
    )


def convert_user_mode_to_domain_model(model: User) -> UserDM:
    return UserDM(
        id=model.id,
        name=model.name,
        email=model.email,
        password=model.password,
        is_active=model.is_active,
    )
