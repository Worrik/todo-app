from fastapi_users import schemas
from pydantic import EmailStr


class UserAuthReadSchema(schemas.BaseUser[int]):
    name: str


class UserAuthCreateSchema(schemas.CreateUpdateDictModel):
    email: EmailStr
    name: str
    password: str
