from dishka import FromDishka
from faststream.rabbit import RabbitRouter

from src.application.tasks.dto import SendTaskStatusUpdateDTO
from src.application.tasks.interactors import SendTaskStatusUpdateInteractor
from src.controllers.ampq.schemas import MailTaskStatusUpdateSchema

ampq_router = RabbitRouter()


@ampq_router.subscriber("send_mail_task_status_update")
async def handle(
    data: MailTaskStatusUpdateSchema,
    interactor: FromDishka[SendTaskStatusUpdateInteractor],
) -> None:
    dto = SendTaskStatusUpdateDTO(id=data.task_id)
    await interactor(dto)
