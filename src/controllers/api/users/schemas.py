from pydantic import BaseModel, EmailStr

from src.application.common.pagination.constants import Empty


class UserSchema(BaseModel):
    id: int
    email: EmailStr
    name: str
    is_active: bool


class UserAuthUpdateSchema(BaseModel):
    email: EmailStr | Empty = Empty.UNSET
    name: str | Empty = Empty.UNSET
    password: str | Empty = Empty.UNSET
