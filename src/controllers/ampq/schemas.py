from pydantic import BaseModel


class MailTaskStatusUpdateSchema(BaseModel):
    task_id: int
