from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends

from src.application.common.pagination.dto import PaginationDTO
from src.application.tasks.dto import GetTaskDTO, NewTaskDTO, UpdateTaskDTO
from src.application.tasks.interactors import (
    CreateTaskInteractor,
    GetPaginatedTasksInteractor,
    GetTaskInteractor,
    UpdateTaskInteractor,
)
from src.controllers.api.tasks.priorities.router import router as priorities_router
from src.controllers.api.tasks.schemas import (
    NewTaskSchema,
    TaskSchema,
    UpdateTaskSchema,
)
from src.controllers.api.tasks.statuses.router import router as statuses_router
from src.controllers.api.users.auth.users import current_active_user

router = APIRouter(dependencies=[Depends(current_active_user)])
router.include_router(statuses_router, prefix="/statuses", tags=["statuses"])
router.include_router(priorities_router, prefix="/priorities", tags=["priorities"])


@router.get("/task/{task_id}/")
@inject
async def get_task(
    task_id: int,
    interactor: FromDishka[GetTaskInteractor],
) -> TaskSchema:
    dto = GetTaskDTO(id=task_id)
    task_dm = await interactor(dto)
    return TaskSchema.from_domain_model(task_dm)


@router.get("/")
@inject
async def get_tasks(
    interactor: FromDishka[GetPaginatedTasksInteractor],
    offset: int | None = None,
    limit: int | None = None,
) -> list[TaskSchema]:
    dto = PaginationDTO(offset=offset, limit=limit)
    tasks_dm = await interactor(dto)
    return [TaskSchema.from_domain_model(task_dm) for task_dm in tasks_dm]


@router.post("/")
@inject
async def create_task(
    data: NewTaskSchema,
    interactor: FromDishka[CreateTaskInteractor],
) -> int:
    dto = NewTaskDTO(
        title=data.title,
        description=data.description,
        assignee_id=data.assignee_id,
        status_id=data.status_id,
        priority_id=data.priority_id,
    )
    return await interactor(dto)


@router.patch("/task/{task_id}/", status_code=204)
@inject
async def update_task(
    task_id: int,
    data: UpdateTaskSchema,
    interactor: FromDishka[UpdateTaskInteractor],
) -> None:
    dto = UpdateTaskDTO(
        id=task_id,
        title=data.title,
        description=data.description,
        assignee_id=data.assignee_id,
        status_id=data.status_id,
        priority_id=data.priority_id,
    )
    await interactor(dto)
