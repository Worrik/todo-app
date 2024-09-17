from fastapi import APIRouter

from src.controllers.api.users.auth.schemas import (
    UserAuthCreateSchema,
    UserAuthReadSchema,
)
from src.controllers.api.users.auth.users import auth_backend, fastapi_users

router = APIRouter()

router.include_router(fastapi_users.get_auth_router(auth_backend))
router.include_router(
    fastapi_users.get_register_router(UserAuthReadSchema, UserAuthCreateSchema)  # type: ignore
)
