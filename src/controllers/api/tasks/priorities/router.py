from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter

from src.application.tasks.dto import DeleteTaskPriorityDTO, NewTaskPriorityDTO
from src.application.tasks.interactors import (
    CreateTaskPriorityInteractor,
    DeleteTaskPriorityInteractor,
    GetTaskPrioritiesInteractor,
)
from src.controllers.api.tasks.priorities.schemas import (
    NewTaskPrioritySchema,
    TaskPrioritySchema,
)

router = APIRouter()


@router.get("/priorities/")
@inject
async def get_priorities(
    interactor: FromDishka[GetTaskPrioritiesInteractor],
) -> list[TaskPrioritySchema]:
    priorities_dm = await interactor()
    return [
        TaskPrioritySchema.from_domain_model(priority_dm)
        for priority_dm in priorities_dm
    ]


@router.post("/priorities/")
@inject
async def create_priority(
    data: NewTaskPrioritySchema,
    interactor: FromDishka[CreateTaskPriorityInteractor],
) -> int:
    dto = NewTaskPriorityDTO(name=data.name, value=data.value)
    return await interactor(dto)


@router.delete("/priorities/priority/{priority_id}/", status_code=204)
@inject
async def delete_priority(
    priority_id: int,
    interactor: FromDishka[DeleteTaskPriorityInteractor],
) -> None:
    dto = DeleteTaskPriorityDTO(id=priority_id)
    await interactor(dto)
