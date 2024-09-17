from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter

from src.application.tasks.dto import DeleteTaskStatusDTO, NewTaskStatusDTO
from src.application.tasks.interactors import (
    CreateTaskStatusInteractor,
    DeleteTaskStatusInteractor,
    GetTaskStatusesInteractor,
)
from src.controllers.api.tasks.statuses.schemas import (
    NewTaskStatusSchema,
    TaskStatusSchema,
)

router = APIRouter()


@router.get("/statuses/")
@inject
async def get_statuses(
    interactor: FromDishka[GetTaskStatusesInteractor],
) -> list[TaskStatusSchema]:
    statuses_dm = await interactor()
    return [TaskStatusSchema.from_domain_model(status_dm) for status_dm in statuses_dm]


@router.post("/statuses/")
@inject
async def create_status(
    data: NewTaskStatusSchema,
    interactor: FromDishka[CreateTaskStatusInteractor],
) -> int:
    dto = NewTaskStatusDTO(name=data.name)
    return await interactor(dto)


@router.delete("/statuses/status/{status_id}/", status_code=204)
@inject
async def delete_status(
    status_id: int,
    interactor: FromDishka[DeleteTaskStatusInteractor],
) -> None:
    dto = DeleteTaskStatusDTO(id=status_id)
    await interactor(dto)
