from typing import AsyncIterable

from dishka import AnyOf, Provider, Scope, from_context, provide
from faststream.broker.core.usecase import BrokerUsecase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.application.common.database.interfaces import DBSession
from src.application.common.messaging.interfaces import StatusUpdateMessagePublisher
from src.application.common.notifications.interfaces import NotificationService
from src.application.tasks.interactors import (
    CreateTaskInteractor,
    CreateTaskPriorityInteractor,
    CreateTaskStatusInteractor,
    DeleteTaskInteractor,
    DeleteTaskPriorityInteractor,
    DeleteTaskStatusInteractor,
    GetPaginatedTasksInteractor,
    GetTaskInteractor,
    GetTaskPrioritiesInteractor,
    GetTaskStatusesInteractor,
    SendTaskStatusUpdateInteractor,
    UpdateTaskInteractor,
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
from src.application.users.interactors import UpdateUserInteractor
from src.application.users.interfaces.repo import UserRepo
from src.config import Config
from src.infrastructure.database.connection import new_session_maker
from src.infrastructure.database.repositories.tasks import TaskRepoImpl
from src.infrastructure.database.repositories.users import UserRepoImpl
from src.infrastructure.gateways.tasks import (
    TaskGateway,
    TaskPriorityGateway,
    TaskStatusGateway,
)
from src.infrastructure.notifications.email_notification import EmailNotificationService


class AppProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)
    broker = from_context(provides=BrokerUsecase, scope=Scope.APP)

    task_gateway = provide(
        TaskGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[TaskGet, TaskCreate, TaskUpdate, TaskDelete],
    )
    task_status_gateway = provide(
        TaskStatusGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[TaskStatusGet, TaskStatusCreate, TaskStatusDelete],
    )
    task_priority_gateway = provide(
        TaskPriorityGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[TaskPriorityGet, TaskPriorityCreate, TaskPriorityDelete],
    )

    task_repo = provide(TaskRepoImpl, scope=Scope.REQUEST, provides=TaskRepo)
    user_repo = provide(UserRepoImpl, scope=Scope.REQUEST, provides=UserRepo)

    get_task_interactor = provide(GetTaskInteractor, scope=Scope.REQUEST)
    get_paginated_tasks_interactor = provide(
        GetPaginatedTasksInteractor,
        scope=Scope.REQUEST,
    )
    create_task_interactor = provide(CreateTaskInteractor, scope=Scope.REQUEST)
    update_task_interactor = provide(UpdateTaskInteractor, scope=Scope.REQUEST)
    delete_task_interactor = provide(DeleteTaskInteractor, scope=Scope.REQUEST)

    get_task_statuses_interactor = provide(
        GetTaskStatusesInteractor, scope=Scope.REQUEST
    )
    create_task_status_interactor = provide(
        CreateTaskStatusInteractor, scope=Scope.REQUEST
    )
    delete_task_status_interactor = provide(
        DeleteTaskStatusInteractor, scope=Scope.REQUEST
    )

    get_task_priorities_interactor = provide(
        GetTaskPrioritiesInteractor, scope=Scope.REQUEST
    )
    create_task_priority_interactor = provide(
        CreateTaskPriorityInteractor, scope=Scope.REQUEST
    )
    delete_task_priority_interactor = provide(
        DeleteTaskPriorityInteractor, scope=Scope.REQUEST
    )

    update_user_interactor = provide(UpdateUserInteractor, scope=Scope.REQUEST)

    send_task_status_update_interactor = provide(
        SendTaskStatusUpdateInteractor, scope=Scope.REQUEST
    )
    notification_service = provide(
        EmailNotificationService, scope=Scope.REQUEST, provides=NotificationService
    )

    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config.postgres)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AnyOf[AsyncSession, DBSession]]:
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.APP, provides=StatusUpdateMessagePublisher)
    def status_update_message_publisher(self, broker: BrokerUsecase):
        return broker.publisher("send_mail_task_status_update")
